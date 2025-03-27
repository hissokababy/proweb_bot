from common.kbds import BACK_TO_MENU_BTN, CONTINUE_BTN, MAILING_BTN

def is_continue_btn(text):
    if text == CONTINUE_BTN:
        return True


def is_main_btn(text):
    if text == BACK_TO_MENU_BTN:
        return True
    
def is_sending_btn(text):
    if text == MAILING_BTN:
        return True
    