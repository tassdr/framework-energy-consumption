from xml.dom import minidom
import re
import time as t
import datetime as dt


'''
Power Profile
'''


def get_amp_value(power_profile, component, state=''):
    """ Retrieve mAh for component in power_profile.xml and convert to Ah """
    if component == 'camera':
        profilename = 'camera.avg'
    elif component == 'flashlight':
        profilename = 'flashlight.on'
    elif component == 'gps':
        profilename = 'gps.on'
    elif component == 'audio':
        profilename = 'dsp.audio'
    elif component == 'video':
        profilename = 'dsp.video'
    elif component == 'bluetooth':
        profilename = 'bluetooth.on'
    elif component == 'phone_scanning':
        profilename = 'radio.scanning'
    else:
        profilename = component
    xmlfile = minidom.parse(power_profile)
    itemlist = xmlfile.getElementsByTagName('item')
    arraylist = xmlfile.getElementsByTagName('array')
    value_index = 0
    for item in itemlist:
        itemname = item.attributes['name'].value
        milliamps = item.childNodes[0].nodeValue
        if profilename == itemname:
            return float(milliamps) / 1000.0
    for arrays in arraylist:
        arrayname = arrays.attributes['name'].value
        if arrayname == 'cpu.speeds':
            valuelist = arrays.getElementsByTagName('value')
            for i in range(valuelist.length):
                value = valuelist.item(i).childNodes[0].nodeValue
                if value == state:
                    value_index = i
        if arrayname == 'cpu.active':
            valuelist = arrays.getElementsByTagName('value')
            milliamps = valuelist.item(value_index).childNodes[0].nodeValue
            return float(milliamps) / 1000.0


'''
Batterystats
'''


def parse_batterystats(app, batterystats_file, power_profile):
    """ Parse Batterystats history and calculate results """
    with open(batterystats_file, 'r') as bs_file:
        voltage_pattern = re.compile('(0|\+\d.*ms).*volt=(\d+)')
        app_pattern = re.compile('(0|\+\d.*ms).*( top|-top|\+top).*"{}"'.format(app))
        screen_pattern = re.compile('(0|\+\d.*ms).*([+-])screen')
        brightness_pattern = re.compile('(0|\+\d.*ms).*brightness=(dark|dim|medium|light|bright)')
        wifi_pattern = re.compile('(0|\+\d.*ms).*([+-])wifi_(running|radio|scan)')
        camera_pattern = re.compile('(0|\+\d.*ms).*([+-])(camera)')
        flashlight_pattern = re.compile('(0|\+\d.*ms).*([+-])(flashlight)')
        gps_pattern = re.compile('(0|\+\d.*ms).*([+-])(gps)')
        audio_pattern = re.compile('(0|\+\d.*ms).*([+-])(audio)')
        video_pattern = re.compile('(0|\+\d.*ms).*([+-])(video)')
        bluetooth_pattern = re.compile('(0|\+\d.*ms).*([+-])(bluetooth)')
        phone_scanning_pattern = re.compile('(0|\+\d.*ms).*([+-])(phone_scanning)')
        time_pattern = re.compile('(0|\+\d.*ms).*')

        f = bs_file.read()
        app_start_time = convert_to_s(re.findall(app_pattern, f)[0][0])
        app_end_time = convert_to_s(re.findall(app_pattern, f)[-1][0])
        voltage = float(re.findall(voltage_pattern, f)[0][1]) / 1000.0

        brightness = None
        screen_start_time = 0
        screen_activation = 0
        wifi_activation = 0

        screen_results = []
        wifi_results = []
        all_results = []

        bs_file.seek(0)
        for line in bs_file:
            current_time = convert_to_s(time_pattern.search(line).group(1))

            if voltage_pattern.search(line):
                voltage = get_voltage(line)

            if screen_activation == 0 and screen_pattern.search(line) and brightness_pattern.search(line):
                screen_state = screen_pattern.search(line).group(2)
                if screen_state == '+' and brightness is None:
                    screen_activation = 1
                    screen_start_time = current_time
                    brightness = brightness_pattern.search(line).group(2)
            elif screen_activation == 0 and screen_pattern.search(line):
                screen_state = screen_pattern.search(line).group(2)
                if screen_state == '+' and brightness is None:
                    screen_activation = 1
                    screen_start_time = app_start_time
                    brightness = 'dark'
            elif screen_activation == 1 and brightness_pattern.search(line):
                if screen_start_time < app_start_time:
                    screen_start_time = app_start_time
                screen_end_time = current_time
                duration = screen_end_time - screen_start_time
                intensity = get_screen_intensity(brightness, power_profile)
                energy_consumption = calculate_energy_usage(intensity, voltage, duration)
                if screen_end_time >= app_start_time and duration != 0:
                    screen_results.append('{},{},{},screen {},{}'.format(
                        screen_start_time - app_start_time, screen_end_time - app_start_time,
                        duration, brightness, energy_consumption))
                brightness = brightness_pattern.search(line).group(2)
                screen_start_time = current_time
            elif screen_activation == 1 and current_time >= app_end_time:
                screen_activation = 0
                if screen_start_time < app_start_time:
                    screen_start_time = app_start_time
                screen_end_time = app_end_time
                duration = screen_end_time - screen_start_time
                intensity = get_screen_intensity(brightness, power_profile)
                energy_consumption = calculate_energy_usage(intensity, voltage, duration)
                if screen_end_time >= app_start_time and duration != 0:
                    screen_results.append('{},{},{},screen {},{}'.format(
                        screen_start_time - app_start_time, screen_end_time - app_start_time,
                        duration, brightness, energy_consumption))
            elif screen_activation == 1 and screen_pattern.search(line):
                screen_state = screen_pattern.search(line).group(2)
                if screen_state == '-':
                    screen_activation = 0
                    if screen_start_time < app_start_time:
                        screen_start_time = app_start_time - app_start_time
                    screen_end_time = current_time - app_start_time
                    duration = screen_end_time - screen_start_time
                    intensity = get_screen_intensity(brightness, power_profile)
                    energy_consumption = calculate_energy_usage(intensity, voltage, duration)
                    if screen_end_time >= app_start_time:
                        screen_results.append('{},{},{},screen {},{}'.format(
                            screen_start_time - app_start_time, screen_end_time - app_start_time,
                            duration, brightness, energy_consumption))

            if wifi_pattern.search(line):
                wifi_state = wifi_pattern.search(line).group(3)
                if wifi_activation == 0 and wifi_pattern.search(line).group(2) == '+' and current_time < app_end_time:
                    wifi_activation = 1
                    old_wifi_state = wifi_state
                    if current_time < app_start_time:
                        wifi_start_time = app_start_time
                    else:
                        wifi_start_time = current_time
                elif wifi_activation == 1 and wifi_state != old_wifi_state and wifi_pattern.search(line).group(2) == '+':
                    if old_wifi_state == 'running':
                        wifi_intensity = get_amp_value(power_profile, 'wifi.on')
                    if old_wifi_state == 'radio':
                        wifi_intensity = get_amp_value(power_profile, 'wifi.active')
                    if old_wifi_state == 'scan':
                        wifi_intensity = get_amp_value(power_profile, 'wifi.scan')
                    wifi_end_time = current_time
                    duration = wifi_end_time - wifi_start_time
                    if duration <= 0:
                        continue
                    energy_consumption = calculate_energy_usage(wifi_intensity, voltage, duration)
                    wifi_results.append('{},{},{},wifi {},{}'.format(
                        wifi_start_time - app_start_time, wifi_end_time - app_start_time, duration,
                        old_wifi_state, energy_consumption))
                    wifi_start_time = current_time
                elif wifi_activation == 1 and wifi_pattern.search(line).group(2) == '-' and current_time < app_end_time:
                    if wifi_state == 'radio':
                        wifi_intensity = get_amp_value(power_profile, 'wifi.active')
                    if wifi_state == 'scan':
                        wifi_intensity = get_amp_value(power_profile, 'wifi.scan')
                    wifi_end_time = current_time
                    duration = wifi_end_time - wifi_start_time
                    if duration <= 0:
                        continue
                    energy_consumption = calculate_energy_usage(wifi_intensity, voltage, duration)
                    wifi_results.append('{},{},{},wifi {},{}'.format(
                        wifi_start_time - app_start_time, wifi_end_time - app_start_time, duration,
                        wifi_state, energy_consumption))
                    wifi_start_time = current_time
                    wifi_state = 'running'
            if wifi_activation == 1 and current_time >= app_end_time:
                wifi_activation = 0
                wifi_end_time = app_end_time
                duration = wifi_end_time - wifi_start_time
                if wifi_state == 'running':
                    wifi_intensity = get_amp_value(power_profile, 'wifi.on')
                if wifi_state == 'radio':
                    wifi_intensity = get_amp_value(power_profile, 'wifi.active')
                if wifi_state == 'scan':
                    wifi_intensity = get_amp_value(power_profile, 'wifi.scan')
                energy_consumption = calculate_energy_usage(wifi_intensity, voltage, duration)
                wifi_results.append('{},{},{},wifi {},{}'.format(
                    wifi_start_time - app_start_time, wifi_end_time - app_start_time, duration,
                    wifi_state, energy_consumption))
        all_results.extend(screen_results + wifi_results)

        component_patterns = [camera_pattern, flashlight_pattern, gps_pattern, audio_pattern, video_pattern,
                              bluetooth_pattern, phone_scanning_pattern]
        component_activation = 0
        component_results = []
        for component_pattern in component_patterns:
            bs_file.seek(0)
            for line in bs_file:
                if component_pattern.search(line):
                    component = component_pattern.search(line).group(3)
                    component_state = component_pattern.search(line).group(2)
                    component_state_time = convert_to_s(component_pattern.search(line).group(1))
                    component_intensity = get_amp_value(power_profile, component)
                    if component_state == '+' and component_state_time < app_end_time:
                        component_activation = 1
                        if component_state_time < app_start_time:
                            component_start_time = app_start_time
                        else:
                            component_start_time = component_state_time
                    elif component_state == '-' and component_state_time < app_end_time:
                        component_activation = 0
                        if (component_start_time < app_end_time) and (component_state_time > app_end_time):
                            component_end_time = app_end_time
                        else:
                            component_end_time = convert_to_s(component_pattern.search(line).group(1))
                        duration = component_end_time - component_start_time
                        if duration != 0:
                            energy_consumption = calculate_energy_usage(component_intensity, voltage, duration)
                            component_results.append('{},{},{},{},{}'.format(
                                component_start_time - app_start_time,
                                component_end_time - app_start_time, duration, component, energy_consumption))
                if component_activation == 1 and current_time >= app_end_time:
                    component_end_time = app_end_time
                    component_activation = 0
                    duration = component_end_time - component_start_time
                    if duration != 0:
                        energy_consumption = calculate_energy_usage(component_intensity, voltage, duration)
                        component_results.append('{},{},{},{},{}'.format(
                            component_start_time - app_start_time,
                            component_end_time - app_start_time, duration, component, energy_consumption))
        all_results.extend(component_results)
    return all_results


def get_voltage(line):
    """ Obtain voltage value """
    pattern = re.compile('volt=(\d+)')
    match = pattern.search(line)
    return float(match.group(1)) / 1000.0


def get_screen_intensity(brightness, power_profile):
    """ Calculate screen intensity """
    intensity_range = get_amp_value(power_profile, 'screen.full') - get_amp_value(power_profile, 'screen.on')
    if brightness == 'dark':
        screen_intensity = get_amp_value(power_profile, 'screen.on')
    elif brightness == 'dim':
        screen_intensity = get_amp_value(power_profile, 'screen.on') + (intensity_range * 0.25)
    elif brightness == 'medium':
        screen_intensity = get_amp_value(power_profile, 'screen.on') + (intensity_range * 0.50)
    elif brightness == 'light':
        screen_intensity = get_amp_value(power_profile, 'screen.on') + (intensity_range * 0.75)
    elif brightness == 'bright':
        screen_intensity = get_amp_value(power_profile, 'screen.full')
    return screen_intensity


def calculate_energy_usage(intensity, voltage, duration):
    return intensity * voltage * duration


def convert_to_s(line):
    """ Convert Batterystats timestamps to seconds """
    milliseconds_pattern = re.compile('\+(\d{3})ms')
    seconds_pattern = re.compile('\+(\d{1,2})s(\d{3})ms')
    minutes_pattern = re.compile('\+(\d{1,2})m(\d{2})s(\d{3})ms')
    hours_pattern = re.compile('\+(\d{1,2})h(\d{1,2})m(\d{2})s(\d{3})ms')
    days_pattern = re.compile('\+(\d)d(\d{1,2})h(\d{1,2})m(\d{2})s(\d{3})ms')

    milliseconds_matches = milliseconds_pattern.search(line)
    seconds_matches = seconds_pattern.search(line)
    minutes_matches = minutes_pattern.search(line)
    hours_matches = hours_pattern.search(line)
    days_matches = days_pattern.search(line)

    SECONDS_IN_MS = 1000.0
    SECONDS_IN_M = 60.0
    SECONDS_IN_H = 3600.0
    SECONDS_IN_D = 86400.0

    if milliseconds_matches:
        s = float(milliseconds_matches.group(1)) / SECONDS_IN_MS
        return s
    elif seconds_matches:
        s = float(seconds_matches.group(2)) / SECONDS_IN_MS
        s += float(seconds_matches.group(1))
        return s
    elif minutes_matches:
        s = float(minutes_matches.group(3)) / SECONDS_IN_MS
        s += float(minutes_matches.group(2))
        s += float(minutes_matches.group(1)) * SECONDS_IN_M
        return s
    elif hours_matches:
        s = float(hours_matches.group(4)) / SECONDS_IN_MS
        s += float(hours_matches.group(3))
        s += float(hours_matches.group(2)) * SECONDS_IN_M
        s += float(hours_matches.group(1)) * SECONDS_IN_H
        return s
    elif days_matches:
        s = float(days_matches.group(5)) / SECONDS_IN_MS
        s += float(days_matches.group(4))
        s += float(days_matches.group(3)) * SECONDS_IN_M
        s += float(days_matches.group(2)) * SECONDS_IN_H
        s += float(days_matches.group(1)) * SECONDS_IN_D
        return s
    else:
        return 0


''' 
Systrace
'''


def parse_systrace(app, systrace_file, logcat, batterystats, power_profile, core_amount):
    """ Parse systrace file and calculate results """
    with open(batterystats, 'r') as bs:
        voltage_pattern = re.compile('(0|\+\d.*ms).*volt=(\d+)')
        voltage = float(re.findall(voltage_pattern, bs.read())[0][1]) / 1000.0

    with open(systrace_file, 'r') as sys:
        f = sys.read()
        pattern = re.compile('(?:<.{3,4}>-\d{1,4}|kworker.+-\d{3}).*\s(\d+\.\d+): (cpu_.*): state=(.*) cpu_id=(\d)')
        unix_time_pattern = re.compile('(\d+\.\d+):\stracing_mark_write:\strace_event_clock_sync:\srealtime_ts=(\d+)')
        logcat_time = parse_logcat(app, logcat)
        systrace_time = float(unix_time_pattern.search(f).group(2))
        start_time = (logcat_time[0] - systrace_time) / 1000 + float(unix_time_pattern.search(f).group(1))
        end_time = (logcat_time[1] - systrace_time) / 1000 + float(unix_time_pattern.search(f).group(1))
        cpu_id_list = []
        results = []

        for i in range(0, core_amount):
            cpu_id_list.append(i)

        cpu_id_list.sort()
        for cpu_id in cpu_id_list:
            matches = pattern.finditer(f)
            found_first_match = 0
            for match in matches:
                current_time = float(match.group(1))
                current_activity = str(match.group(2))
                current_state = str(match.group(3))
                current_cpu_id = int(match.group(4))
                if current_time < start_time:
                    pass
                else:
                    if (found_first_match == 0) and (current_cpu_id == cpu_id) and current_time > start_time:
                        time = start_time
                        duration = current_time - time
                        activity = 'cpu_idle'
                        cpu_intensity = get_amp_value(power_profile, 'cpu.idle')
                        energy_consumption = calculate_energy_usage(cpu_intensity, voltage, duration)
                        results.append('{},{},{},core {} {} start,{}'.format
                                       (time - start_time, current_time - start_time,
                                        duration, cpu_id, activity, energy_consumption))
                        time = current_time
                        activity = current_activity
                        state = current_state
                        cpu_id = current_cpu_id
                        found_first_match = 1
                    elif found_first_match == 1 and (current_cpu_id == cpu_id) and current_time < end_time:
                        if (current_activity == activity) and (current_state == state):
                            pass
                        elif current_activity == activity == 'cpu_idle':
                            pass
                        elif current_activity == 'cpu_frequency' and activity == 'cpu_idle':
                            duration = current_time - time
                            cpu_intensity = get_amp_value(power_profile, 'cpu.idle')
                            energy_consumption = calculate_energy_usage(cpu_intensity, voltage, duration)
                            results.append('{},{},{},core {} {},{}'.format
                                           (time - start_time, current_time - start_time,
                                            duration, cpu_id, activity, energy_consumption))
                            time = current_time
                            activity = current_activity
                            state = current_state
                        elif (current_activity == activity == 'cpu_frequency') and (current_state == state):
                            pass
                        elif (current_activity == activity == 'cpu_frequency') and (current_state != state):
                            duration = current_time - time
                            cpu_intensity = get_amp_value(power_profile, activity, state)
                            energy_consumption = calculate_energy_usage(cpu_intensity, voltage, duration)
                            results.append('{},{},{},core {} {},{}'.format
                                           (time - start_time, current_time - start_time,
                                            duration, cpu_id, activity, energy_consumption))
                            time = current_time
                            activity = current_activity
                            state = current_state
                        elif current_activity == 'cpu_idle' and activity == 'cpu_frequency':
                            duration = current_time - time
                            cpu_intensity = get_amp_value(power_profile, activity, state)
                            energy_consumption = calculate_energy_usage(cpu_intensity, voltage, duration)
                            results.append('{},{},{},core {} {},{}'.format
                                           (time - start_time, current_time - start_time,
                                            duration, cpu_id, activity, energy_consumption))
                            time = current_time
                            activity = current_activity
                            state = current_state
                if found_first_match == 1 and current_time >= end_time:
                    duration = end_time - time
                    if current_activity == 'cpu_idle':
                        cpu_intensity = get_amp_value(power_profile, 'cpu.idle')
                    else:
                        cpu_intensity = get_amp_value(power_profile, activity, state)
                    energy_consumption = calculate_energy_usage(cpu_intensity, voltage, duration)
                    results.append('{},{},{},core {} {},{}'.format
                                   (time - start_time, end_time - start_time,
                                    duration, cpu_id, activity, energy_consumption))
                    break
                if found_first_match == 0 and current_time >= end_time:
                    duration = end_time - start_time
                    activity = 'cpu_idle'
                    cpu_intensity = get_amp_value(power_profile, 'cpu.idle')
                    energy_consumption = calculate_energy_usage(cpu_intensity, voltage, duration)
                    results.append('{},{},{},core {} {},{}'.format
                                   (start_time - start_time, end_time - start_time,
                                    duration, cpu_id, activity, energy_consumption))
                    break
    return results


''' Logcat '''


def parse_logcat(app, logcat_file):
    """ Obtain app start and end times from logcat """
    with open(logcat_file, 'r') as f:
        logcat = f.read()
        app_start_pattern = re.compile(
            '(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}).(\d{3}).*ActivityManager:\sDisplayed\s(%s)' % app)
        app_start_date = re.findall(app_start_pattern, logcat)[0][0]
        year = dt.datetime.now().year
        time_tuple = t.strptime('{}-{}'.format(year, app_start_date), '%Y-%m-%d %H:%M:%S')
        unix_start_time = int(t.mktime(time_tuple)) * 1000 + int(app_start_pattern.search(logcat).group(2))

        app_stop_pattern = re.compile(
            '(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}).(\d{3}).*ActivityManager:\sForce\sstopping\s(%s)' % app)
        app_stop_date = re.findall(app_stop_pattern, logcat)[-1][0]
        time_tuple = t.strptime('{}-{}'.format(year, app_stop_date), '%Y-%m-%d %H:%M:%S')
        unix_end_time = int(t.mktime(time_tuple)) * 1000 + int(app_stop_pattern.search(logcat).group(2))
        return unix_start_time, unix_end_time
