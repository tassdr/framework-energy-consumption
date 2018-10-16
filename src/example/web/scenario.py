import os
import time


class Scenario:
    BUTTON1_CHROME_X = 759
    BUTTON1_CHROME_Y = 2236
    BUTTON2_CHROME_X = 254
    BUTTON2_CHROME_Y = 2273

    url = ""

    BUTTON_SIGNIN_X = 0
    BUTTON_SIGNIN_Y = 0
    BUTTON_EMAIL_X = 0
    BUTTON_EMAIL_Y = 0
    BUTTON_PASSWORD_X = 0
    BUTTON_PASSWORD_Y = 0
    BUTTON_SIGNIN2_X = 0
    BUTTON_SIGNIN2_Y = 0
    BUTTON_ARTICLE_X = 0
    BUTTON_ARTICLE_Y = 0
    BUTTON_ARTICLE_GENERAL_X = 0
    BUTTON_ARTICLE_GENERAL_Y = 0
    BUTTON_ARTICLE_TITLE_Y = 0
    BUTTON_ARTICLE_ABOUT_Y = 0
    BUTTON_ARTICLE_DESCRIPTION_Y = 0
    BUTTON_ARTICLE_TAGS_Y = 0
    BUTTON_ARTICLE_PUBLISH_X = 0
    BUTTON_ARTICLE_PUBLISH_Y = 0

    def __init__(self, url, BUTTON_SIGNIN_X, BUTTON_SIGNIN_Y, BUTTON_EMAIL_X, BUTTON_EMAIL_Y, BUTTON_PASSWORD_X,
                 BUTTON_PASSWORD_Y, BUTTON_SIGNIN2_X, BUTTON_SIGNIN2_Y, BUTTON_ARTICLE_X, BUTTON_ARTICLE_Y,
                 BUTTON_ARTICLE_GENERAL_X, BUTTON_ARTICLE_TITLE_Y, BUTTON_ARTICLE_ABOUT_Y, BUTTON_ARTICLE_DESCRIPTION_Y,
                 BUTTON_ARTICLE_TAGS_Y, BUTTON_ARTICLE_PUBLISH_X, BUTTON_ARTICLE_PUBLISH_Y):
        self.url = url
        self.BUTTON_SIGNIN_X = BUTTON_SIGNIN_X
        self.BUTTON_SIGNIN_Y = BUTTON_SIGNIN_Y
        self.BUTTON_EMAIL_X = BUTTON_EMAIL_X
        self.BUTTON_EMAIL_Y = BUTTON_EMAIL_Y
        self.BUTTON_PASSWORD_X = BUTTON_PASSWORD_X
        self.BUTTON_PASSWORD_Y = BUTTON_PASSWORD_Y
        self.BUTTON_SIGNIN2_X = BUTTON_SIGNIN2_X
        self.BUTTON_SIGNIN2_Y = BUTTON_SIGNIN2_Y
        self.BUTTON_ARTICLE_X = BUTTON_ARTICLE_X
        self.BUTTON_ARTICLE_Y = BUTTON_ARTICLE_Y
        self.BUTTON_ARTICLE_GENERAL_X = BUTTON_ARTICLE_GENERAL_X
        self.BUTTON_ARTICLE_TITLE_Y = BUTTON_ARTICLE_TITLE_Y
        self.BUTTON_ARTICLE_ABOUT_Y = BUTTON_ARTICLE_ABOUT_Y
        self.BUTTON_ARTICLE_DESCRIPTION_Y = BUTTON_ARTICLE_DESCRIPTION_Y
        self.BUTTON_ARTICLE_TAGS_Y = BUTTON_ARTICLE_TAGS_Y
        self.BUTTON_ARTICLE_PUBLISH_X = BUTTON_ARTICLE_PUBLISH_X
        self.BUTTON_ARTICLE_PUBLISH_Y = BUTTON_ARTICLE_PUBLISH_Y

    def processUrl(self):
        # command to open the url in Chrome
        adbCommand1 = "adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main -d " + self.url + " --ez create_new_tab true"

        # command to clear the Chrome application data
        adbCommand2 = "adb shell pm clear com.android.chrome"

        os.system(adbCommand2)

        os.system(adbCommand1)
        time.sleep(1.5)

        # disable the Chrome welcome screen
        os.system("adb shell input tap %d %d" % (self.BUTTON1_CHROME_X, self.BUTTON1_CHROME_Y))
        time.sleep(0.5)
        time.sleep(0.5)
        os.system("adb shell input tap %d %d" % (self.BUTTON2_CHROME_X, self.BUTTON2_CHROME_Y))
        time.sleep(0.5)

        # wait for the page to load
        time.sleep(8)

        # go to sign in page
        os.system("adb shell input tap %d %d" % (self.BUTTON_SIGNIN_X, self.BUTTON_SIGNIN_Y))

        # insert email
        os.system("adb shell input tap %d %d" % (self.BUTTON_EMAIL_X, self.BUTTON_EMAIL_Y))
        os.system("adb shell input text 'lucag.8595@gmail.com'")

        # insert password
        os.system("adb shell input tap %d %d" % (self.BUTTON_PASSWORD_X, self.BUTTON_PASSWORD_Y))
        os.system("adb shell input text 'ciaociao'")

        if self.url == "http://192.168.43.164:4201":
            os.system("adb shell input swipe 500 1000 300 300")
            os.system("adb shell input tap %d %d" % (1258, 971))
        else:
            # sign in
            os.system("adb shell input tap %d %d" % (self.BUTTON_SIGNIN2_X, self.BUTTON_SIGNIN2_Y))

        # wait for the page to load
        time.sleep(5)

        # go to create article page
        os.system("adb shell input tap %d %d" % (self.BUTTON_ARTICLE_X, self.BUTTON_ARTICLE_Y))

        # wait for the page to load
        time.sleep(5)

        # insert article title
        os.system("adb shell input tap %d %d" % (self.BUTTON_ARTICLE_GENERAL_X, self.BUTTON_ARTICLE_TITLE_Y))
        os.system("adb shell input text 'My%sfirst%sarticle'")

        # insert article about
        os.system("adb shell input tap %d %d" % (self.BUTTON_ARTICLE_GENERAL_X, self.BUTTON_ARTICLE_ABOUT_Y))
        os.system("adb shell input text 'This%sis%san%sexperiment%sarticle'")

        # insert article description
        os.system("adb shell input tap %d %d" % (self.BUTTON_ARTICLE_GENERAL_X, self.BUTTON_ARTICLE_DESCRIPTION_Y))
        os.system(
            "adb shell input text 'Hey%sthere!%sI%sam%sso%shappy%sto%swrite%smy%sfirst%sarticle%sfor%sthe%sgreen%slab%scourse!'")

        os.system("adb shell input swipe 500 1000 300 300")

        # insert article tags
        os.system("adb shell input tap %d %d" % (self.BUTTON_ARTICLE_GENERAL_X, self.BUTTON_ARTICLE_TAGS_Y))
        os.system("adb shell input text 'green_lab'")

        # publish article
        os.system("adb shell input tap %d %d" % (self.BUTTON_ARTICLE_PUBLISH_X, self.BUTTON_ARTICLE_PUBLISH_Y))

        # wait for the page to load
        time.sleep(5)

        os.system(adbCommand2)
