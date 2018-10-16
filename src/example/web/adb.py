import os
import time

import scenario

URLS = ["http://192.168.43.164:4201", "http://192.168.43.164:3449", "http://192.168.43.164:9999", "http://192.168.43.164:3006", "http://192.168.43.164:8085", "http://192.168.43.164:3000", "http://192.168.43.164:8080"]
BUTTON1_CHROME_X = 759
BUTTON1_CHROME_Y = 2236
BUTTON2_CHROME_X = 254
BUTTON2_CHROME_Y = 2273


def main(device, *args, **kwargs):

	# for url in URLS:
	# 	if(url == "http://192.168.43.164:4000" or url == "http://192.168.43.164:3449"):
	# 		process(url, 1105, 327, 621, 579, 621, 704, 924, 776, 968, 324, 403, 436, 525, 1139, 457, 1330, 599)
	# 	else:
	# 		process(url, 1030, 404, 214, 979, 219, 1239, 1284, 1403, 732, 549, 201, 784, 1040, 1274, 1286, 1114, 977)
	angularngrx = Scenario("http://192.168.43.164:4000", 1105, 327, 621, 579, 621, 704, 924, 776, 968, 324, 403, 436, 525, 1139, 457, 1330, 599)
	angularngrx.processUrl()



def process(url, BUTTON_SIGNIN_X, BUTTON_SIGNIN_Y, BUTTON_EMAIL_X, BUTTON_EMAIL_Y, BUTTON_PASSWORD_X,
			BUTTON_PASSWORD_Y, BUTTON_SIGNIN2_X, BUTTON_SIGNIN2_Y, BUTTON_ARTICLE_X, BUTTON_ARTICLE_Y,
			BUTTON_ARTICLE_GENERAL_X, BUTTON_ARTICLE_TITLE_Y, BUTTON_ARTICLE_ABOUT_Y, BUTTON_ARTICLE_DESCRIPTION_Y,
			BUTTON_ARTICLE_TAGS_Y, BUTTON_ARTICLE_PUBLISH_X, BUTTON_ARTICLE_PUBLISH_Y):

	#command to open the url in Chrome
    adbCommand1 = "adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main -d "+url+" --ez create_new_tab true"

    #command to clear the Chrome application data
    adbCommand2 = "adb shell pm clear com.android.chrome"

    os.system(adbCommand2)

    os.system(adbCommand1)
    time.sleep(1.5)

    #disable the Chrome welcome screen
    os.system("adb shell input tap %d %d" % (BUTTON1_CHROME_X, BUTTON1_CHROME_Y))
    time.sleep(0.5)
    time.sleep(0.5)
    os.system("adb shell input tap %d %d" % (BUTTON2_CHROME_X, BUTTON2_CHROME_Y))
    time.sleep(0.5)

    #wait for the page to load
    time.sleep(8)

    #go to sign in page
    os.system("adb shell input tap %d %d" % (BUTTON_SIGNIN_X, BUTTON_SIGNIN_Y))

    #insert email
    os.system("adb shell input tap %d %d" % (BUTTON_EMAIL_X, BUTTON_EMAIL_Y))
    os.system("adb shell input text 'lucag.8595@gmail.com'")

    #insert password
    os.system("adb shell input tap %d %d" % (BUTTON_PASSWORD_X, BUTTON_PASSWORD_Y))
    os.system("adb shell input text 'ciaociao'")

    if(url == "http://192.168.43.164:4201"):
    	os.system("adb shell input swipe 500 1000 300 300")
    	os.system("adb shell input tap %d %d" % (1258, 971))
    else:
    	#sign in
    	os.system("adb shell input tap %d %d" % (BUTTON_SIGNIN2_X, BUTTON_SIGNIN2_Y))

    #wait for the page to load
    time.sleep(5)

    #go to create article page
    os.system("adb shell input tap %d %d" % (BUTTON_ARTICLE_X, BUTTON_ARTICLE_Y))

    #wait for the page to load
    time.sleep(5)

    #insert article title
    os.system("adb shell input tap %d %d" % (BUTTON_ARTICLE_GENERAL_X, BUTTON_ARTICLE_TITLE_Y))
    os.system("adb shell input text 'My%sfirst%sarticle'")

    #insert article about
    os.system("adb shell input tap %d %d" % (BUTTON_ARTICLE_GENERAL_X, BUTTON_ARTICLE_ABOUT_Y))
    os.system("adb shell input text 'This%sis%san%sexperiment%sarticle'")

    #insert article description
    os.system("adb shell input tap %d %d" % (BUTTON_ARTICLE_GENERAL_X, BUTTON_ARTICLE_DESCRIPTION_Y))
    os.system("adb shell input text 'Hey%sthere!%sI%sam%sso%shappy%sto%swrite%smy%sfirst%sarticle%sfor%sthe%sgreen%slab%scourse!'")

    os.system("adb shell input swipe 500 1000 300 300")

    #insert article tags
    os.system("adb shell input tap %d %d" % (BUTTON_ARTICLE_GENERAL_X, BUTTON_ARTICLE_TAGS_Y))
    os.system("adb shell input text 'green_lab'")

    #publish article
    os.system("adb shell input tap %d %d" % (BUTTON_ARTICLE_PUBLISH_X, BUTTON_ARTICLE_PUBLISH_Y))

    #wait for the page to load
    time.sleep(5)

    os.system(adbCommand2)





			