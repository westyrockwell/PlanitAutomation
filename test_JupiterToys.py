import os
import re
import time
import logging
from tokenize import Floatnumber
import pytest

from conftest import DriverWrap
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import common
from selenium.webdriver.common.by import By

g = None

logging.basicConfig(filename="PlanitTest.log",
    format='%(asctime)s %(message)s',
    filemode='a')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

os.environ['PATH'] += r"C:/SeleniumDrivers"
print("Added Selenium Drivers to Path environment variable.")

def logInfo(msg):
    print(msg)
    log.info(msg)

def logDebug(msg):
    print(msg)
    log.debug(msg)

def logException(msg):
    print(msg)
    log.exception(msg)

def validateSubmissionMessage():
    global driver
    logInfo(f"validateSubmissionMessage()")
    isMessageValid = False
    try:
         #WebDriverWait(30).until(EC.text_to_be_present_in_element(
                #(By.CLASS_NAME, 'alert alert-success'),
                #'Thanks Donald, we appreciate your feedback.'))
        
        #successAlert = g.driver.find_element(by=By.CLASS_NAME, value='alert alert-success')
        #thanks = driver.find_element(by=By.CLASS_NAME, value="ng-binding")
        #(By.CLASS_NAME, 'ng-binding'),
        
        WebDriverWait(g.driver, 30).until(EC.text_to_be_present_in_element(
            (By.XPATH, '/html/body/div[2]/div/div/strong'),
            'Thanks Donald'))        
        logInfo('validation succeeded')        
        isMessageValid = True        
    except common.exceptions.TimeoutException:
        logException('validation failed')
    except common.exceptions.NoSuchElementException:
        logException('validation failed')
    assert isMessageValid

def validateError(identifier=None):
    logInfo(f"validateError() identifier is {identifier}")
    errorID = identifier + '-err'
    errorFound = False
    try:
        errMessage = g.driver.find_element(by=By.ID, value=errorID)
#        WebDriverWait(30).until(EC.visibility_of_any_elements_located(
#           (By.ID, errorID)))
    except common.exceptions.TimeoutException:
        logDebug(f"{errorID} not found; Timed out.")
    except common.exceptions.NoSuchElementException:
        logDebug(f"{errorID} not found; No such element.")
    except: 
        logException("unexpected exception")
    else:
        log.info(f"{errorID}  found!")
        errorFound = True
    return errorFound

def validateSuccess(identifier=None):
    print(f"validateSuccess() identifier is {identifier}")
    errorID = identifier + '-err'
    errorFound = False
    try:
        errMessage = g.driver.find_element(by=By.ID, value=errorID)
#        WebDriverWait(30).until(EC.visibility_of_any_elements_located(
#           (By.ID, errorID)))
    except common.exceptions.TimeoutException:
        print(f"{errorID} not found")
        logDebug(f"{errorID} not found; Timed out.")
    except common.exceptions.NoSuchElementException:
        print(f"{errorID} not found")
        logDebug(f"{errorID} not found; No such element.")
    except: 
        print("unexpected exception!")
        logDebug("unexpected exception")
        log.exception("unexpected exception")
    else:
        print(f"{errorID}  found!")
        log.info(f"{errorID}  found!")
        errorFound = True
    return (not errorFound)

def validateErrorMessageFound(identifier):
    return findErrorMessage(identifier, expectSuccess=True)

def validateErrorMessageNotFound(identifier):
    return not findErrorMessage(identifier, expectSuccess=False)

def findErrorMessage(identifier, expectSuccess):
    errorID = identifier + '-err'    
    logInfo(f"findErrorMessage() identifier is {identifier} errorID is {errorID} expectSuccess is {expectSuccess}")
    errorFound = False
    try:
        foreNameErr = g.driver.find_element(by=By.ID, value=errorID)
#        logInfo("waiting!")
#        WebDriverWait(30).until(EC.visibility_of_any_elements_located(
#           (By.ID, errorID)))
    except common.exceptions.TimeoutException:
        logDebug(f"{errorID} not found! Timed out looking.")
    except common.exceptions.NoSuchElementException:
        logDebug(f"{errorID} not found! No such element.")
    except: 
        logException("unexpected exception!")
    else:
        errorFound = True
        logInfo(f"{errorID} found!")
    return errorFound    

def populateField(field=None):
    logInfo(f"populateField {field}")
    ctrl = g.driver.find_element(by=By.ID, value=field)
    logInfo(f"type(ctrl) is {type(ctrl)}")
    keysToSend = None
    if field == 'forename':
        keysToSend = 'Donald'
    elif field == 'email':
        keysToSend = 'nzrockwell@gmail.com'
    elif  field == 'message':
        keysToSend = 'A Golden Opportunity!'
    else:
        errMsg = f"{__name__}.populateField() needs implementing for field={field}"
        logDebug(errMsg)
        raise errMsg
    logInfo(f"keysToSend is {keysToSend}")
    ctrl.send_keys(keysToSend)

def populateMandatoryFields():
    logInfo(f"populateMandatoryFields()")    
    for field in g.mandatoryFields:
        populateField(field)

def validateNoErrors():
    logInfo(f"validateNoErrors()")        
    for field in g.mandatoryFields:
        assert(validateErrorMessageNotFound(field))

def validateErrors():
    logInfo(f"validateErrors()")            
    for field in g.mandatoryFields:
        assert(validateErrorMessageFound(field))

def clickSubmitButton():
    logInfo(f"clickSubmitButton()")
    #submitButton = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/form/div/a')
    submitButton = g.driver.find_element(by=By.LINK_TEXT, value='Submit')
    submitButton.click()

def clickElementByXpath(xpath=None):
    logInfo(f"clickElementByXpath() xpath is {xpath}")
    elemToClick = g.driver.find_element(by=By.XPATH, value=xpath)
    elemToClick.click()
    time.sleep(5)

def getElementValueByXpath(xpath=None):
    logInfo(f"getElementValueByXpath() xpath is {xpath}")
    elem = g.driver.find_element(by=By.XPATH, value=xpath)
    val = elem.get_attribute('value')
    logInfo(f"Value of element is {val}")
    return val    

def validateElementValueByXpath(xpath=None, expectedValue=None):
    logInfo(f"validateElementValueByXpath() xpath is {xpath}")
    elem = g.driver.find_element(by=By.XPATH, value=xpath)
    val = elem.get_attribute('value')
    logInfo(f"Value of element is {val} and expectedValue is {expectedValue}")    
    assert val == expectedValue

def validateElementTextByXpath(xpath=None, expectedText=None):
    logInfo(f"validateElementTextByXpath() xpath is {xpath}")
    elem = g.driver.find_element(by=By.XPATH, value=xpath)
    elemText = elem.text
    logInfo(f"Text of element is {elemText} and expectedValue is {expectedText}")    
    assert elemText == expectedText

def validateNumberInElementTextByXpath(xpath=None, expectedNumberAsString=None):
    logInfo(f"validateElementTextByXpath() xpath is {xpath}")
    elemText = g.driver.find_element(by=By.XPATH, value=xpath).text
    logInfo(f"Text of element is {elemText} and expectedNumberAsString is {expectedNumberAsString}")        
    numberList = re.findall(r"\d+\.\d+", elemText)
    floatNumberAsString = numberList[0]
    logInfo(f"float number from element text is {floatNumberAsString}")
    assert floatNumberAsString == expectedNumberAsString

def goToShopPage():
    logInfo(f"goToShopPage()")    
    shopLink = g.driver.find_element(by=By.LINK_TEXT, value='Shop')
    shopLink.click()

def goToHomePage():
    logInfo(f"goToHomePage()")    
    homeLink = g.driver.find_element(by=By.LINK_TEXT, value='Home')
    homeLink.click()
    
def goToContactPage():
    logInfo(f"goToContactPage()")    
    #ContactLink = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div/ul[1]/li[3]/a')
    contactLink = g.driver.find_element(by=By.LINK_TEXT, value='Contact')
    contactLink.click()

def getDriver():
    logInfo(f"getDriver()")    
    global g
    if g is None: 
        g = DriverWrap()
        #logInfo(f"Using driver {DriverWrap.driver.name}")
        url = "https://jupiter.cloud.planittesting.com"
        g.driver.get(url)
        logInfo(f"Testing url {url}")    
        g.driver.implicitly_wait(3) #longer for real testing
    else: 
        g.driver.refresh()
        #g.driver.get(g.driver.getCurrentURL())

def doSetup():
    logInfo(f"doSetup()")
    global g
    getDriver()
    g.mandatoryFields = ["forename", "email", "message"]
    logInfo(f"mandatory fields are {g.mandatoryFields}")    

def doTeardown():
    global g
    logInfo(f"doTeardown()")
    getDriver()
   
def testCase1():
    logInfo("Test case 1")
    doSetup()
    # 1. From the home page go to contact page 
    goToContactPage()
    # 2. Click submit button 
    clickSubmitButton()
    # 3. Validate errors 
    time.sleep(5) # just slow it down to see errors
    validateErrors()
    # 4. Populate mandatory fields 
    populateMandatoryFields()
    # 5. Validate errors are gone 
    time.sleep(5) # just slow it down to see no errors    
    validateNoErrors()
    doTeardown()
    
def testCase2():
    logInfo("Test case 2 -- Five repetitions")    
    for rep in range(0, 5):
        doSetup()
        #1. From the home page go to contact page 
        goToHomePage()
        goToContactPage()
        #2. Populate mandatory fields 
        populateMandatoryFields()
        #3. Click submit button 
        clickSubmitButton()    
        #4. Validate successful submission message     
        validateSubmissionMessage()
        doTeardown()

def testCase3(): 
    logInfo("Test case 3")    
    doSetup()
    #1. From the home page go to shop page
    goToHomePage()
    goToShopPage()
    
    itemsToBuy = {"Funny Cow":2, "Fluffy Bunny":1}
    
    productList = g.driver.find_element(by=By.CLASS_NAME, value='products')
    items = productList.find_elements(by=By.TAG_NAME, value="li")
    for item in items:
        # logInfo(item.get_attribute("innerHTML"))
        # logInfo(f"{item.text}")
        productText = item.find_element(by=By.CLASS_NAME, value='product-title').text
        if productText in itemsToBuy:
            logInfo(f"found {productText} in itemsToBuy")    
            btn = item.find_element(by=By.LINK_TEXT, value='Buy')
            quantity = int(itemsToBuy[productText])
            for i in range(0, quantity):
                btn.click()
                time.sleep(.1)
   
    #4. Click the cart menu
    xpath = r'//*[@id="nav-cart"]/a'
    clickElementByXpath(xpath)    
    
    #5. Verify the items are in te cart
    columnHeaders = {}    
    form = g.driver.find_element(by=By.NAME, value='form')
    table = form.find_element(by=By.CLASS_NAME, value='table')
    headers = table.find_elements(by=By.TAG_NAME, value='th')
    col = 1
    for header in headers: 
        logInfo(f"{header.text}")        
        columnHeaders[header.text] = col
        col += 1
         
    itemNumber = 1
    cartItems = table.find_elements(by=By.CLASS_NAME, value='cart-item')
    for item in cartItems:
        # logInfo(item.get_attribute("innerHTML"))
        logInfo(f"{itemNumber} {item.text}")
        image = item.find_element(by=By.TAG_NAME, value='img')
        imageText = image.find_element(by=By.XPATH, value='./..').text
        logInfo(f"{imageText}")        
        if imageText in itemsToBuy:
            logInfo(f"found {imageText} in itemsToBuy")
            quantityExpected = itemsToBuy[imageText]
            logInfo(f"quantityExpected {quantityExpected}")        
            quantityColumn = columnHeaders['Quantity']
            logInfo(f"quantityColumn {quantityColumn}")        
            xpath = r'//table/tbody/tr[' 
            xpath += f"{itemNumber}"
            xpath += r']/td['
            xpath += f"{quantityColumn}"
            xpath += r']/input'
            logInfo(f"{xpath}")        
            validateElementValueByXpath(xpath, f"{quantityExpected}")
        itemNumber += 1
    doTeardown()

def testCase4():
    logInfo("Test case 4")    
    doSetup()
    #1. Buy 2 Stuffed Frog, 5 Fluffy Bunny, 3 Valentine Bear
    goToHomePage()
    goToShopPage()
    itemsToBuy = {"Stuffed Frog":2, "Fluffy Bunny":5, "Teddy Bear":3}
    pricesOfItems = {}
    
    productList = g.driver.find_element(by=By.CLASS_NAME, value='products')
    items = productList.find_elements(by=By.TAG_NAME, value="li")
    for item in items:
        # logInfo(item.get_attribute("innerHTML"))
        # logInfo(f"{item.text}")
        productText = item.find_element(by=By.CLASS_NAME, value='product-title').text
        if productText in itemsToBuy:
            logInfo(f"found {productText} in itemsToBuy")    
            price = item.find_element(by=By.CLASS_NAME, value='product-price').text
            pricesOfItems[productText] = price
            logInfo(f"price is {price}")    
            btn = item.find_element(by=By.LINK_TEXT, value='Buy')
            quantity = int(itemsToBuy[productText])
            for i in range(0, quantity):
                btn.click()
                time.sleep(.1)

    #2. Go to the cart page
    xpath = r'//*[@id="nav-cart"]/a'
    clickElementByXpath(xpath)    

    #3. Verify the price for each product
    columnHeaders = {}    
    form = g.driver.find_element(by=By.NAME, value='form')
    table = form.find_element(by=By.CLASS_NAME, value='table')
    headers = table.find_elements(by=By.TAG_NAME, value='th')
    col = 1
    for header in headers: 
        logInfo(f"{header.text}")        
        columnHeaders[header.text] = col
        col += 1
         
    itemNumber = 1
    cartItems = table.find_elements(by=By.CLASS_NAME, value='cart-item')
    for item in cartItems:
        # logInfo(item.get_attribute("innerHTML"))
        logInfo(f"{itemNumber} {item.text}")
        image = item.find_element(by=By.TAG_NAME, value='img')
        imageText = image.find_element(by=By.XPATH, value='./..').text
        logInfo(f"{imageText}")        
        if imageText in pricesOfItems:
            logInfo(f"found {imageText} in pricesOfItems")
            expectedPrice = pricesOfItems[imageText]
            logInfo(f"expectedPrice {expectedPrice}")        
            priceColumn = columnHeaders['Price']
            logInfo(f"priceColumn {priceColumn}")        
            xpath = r'//table/tbody/tr[' 
            xpath += f"{itemNumber}"
            xpath += r']/td['
            xpath += f"{priceColumn}"
            xpath += r']'
            logInfo(f"{xpath}")        
            validateElementTextByXpath(xpath, expectedPrice)
        itemNumber += 1

    #4. Verify that each product's sub total = product price * quantity
    sumOfSubTotals = 0
    itemNumber = 1
    for item in cartItems:
        logInfo(f"{itemNumber} {item.text}")
        image = item.find_element(by=By.TAG_NAME, value='img')
        imageText = image.find_element(by=By.XPATH, value='./..').text
        logInfo(f"{imageText}")        
        if imageText in pricesOfItems:
            logInfo(f"found {imageText} in pricesOfItems")            
            if imageText in itemsToBuy:
                logInfo(f"found {imageText} in itemsToBuy")                
                quantity = itemsToBuy[imageText]
                logInfo(f"quantity {quantity}")   
                expectedPrice = pricesOfItems[imageText]
                logInfo(f"expectedPrice {expectedPrice}")                   
                subtotalColumn = columnHeaders['Subtotal']
                xpath = r'//table/tbody/tr[' 
                xpath += f"{itemNumber}"
                xpath += r']/td['
                xpath += f"{subtotalColumn}"
                xpath += r']'
                logInfo(f"{xpath}")
                expectedPriceAmount = float(expectedPrice.replace('$', ''))
                logInfo(f"expectedPriceAmount {expectedPriceAmount}")                
                expectedSubTotal = '$' + str(expectedPriceAmount * quantity)
                logInfo(f"expectedSubTotal {expectedSubTotal}")
                validateElementTextByXpath(xpath, expectedSubTotal)
                expectedSubTotalAmount = float(expectedSubTotal.replace('$', ''))
                logInfo(f"expectedSubTotalAmount {expectedSubTotalAmount}")                
                sumOfSubTotals += expectedSubTotalAmount
                logInfo(f"sumOfSubTotals {sumOfSubTotals}")
        itemNumber += 1        
    
    #5. Verify that total = sum(sub totals)
    xpath = r'//table/tfoot/tr[1]/td/strong'
    validateNumberInElementTextByXpath(xpath, f"{sumOfSubTotals}")
    doTeardown()
    # if you add more test methods move finishTesting call to end of last one.
    finishTesting()
 
def finishTesting():
    g.driver.close()
    g.driver.quit()
     
def main():
    assert True
    testCase1()
    testCase2()
    testCase3()
    testCase4()
    finishTesting()
    
if __name__=="__main__":
    main()
