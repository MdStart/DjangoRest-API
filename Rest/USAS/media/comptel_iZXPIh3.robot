*** Settings ***
Library  Selenium2Library


*** Test Cases ***
TestCase1
    Open Browser    http://www.comptel.com/    ff
    Close Browser

TestCase2
    Open Browser    http://www.comptel.com/    ff
