from common.kbds import BACK_TO_MENU_BTN, CONTINUE_BTN, MAILING_BTN, GROUP_MAILING_BTN, PRIVATE_MAILING_BTN

def is_continue_btn(text):
    if text == CONTINUE_BTN:
        return True


def is_main_btn(text):
    if text == BACK_TO_MENU_BTN:
        return True
    
def is_sending_btn(text):
    if text == MAILING_BTN:
        return True


def is_group_mailing_btn(text):
    if text == GROUP_MAILING_BTN:
        return True

def is_private_mailing_btn(text):
    if text == PRIVATE_MAILING_BTN:
        return True
