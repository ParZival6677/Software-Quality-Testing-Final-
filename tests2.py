import time
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Logging setup: all INFO and above messages will be recorded in the test_log.log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    filename='test_log.log',
    filemode='w'
)
logger = logging.getLogger(__name__)

BASE_URL = "https://demowebshop.tricentis.com/"

# Fixture for initializing WebDriver for browsers: Chrome, Firefox, Edge
@pytest.fixture(params=["chrome", "firefox", "edge"])
def driver(request):
    browser = request.param
    logger.info(f"Initializing driver for browser: {browser}")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        drv = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        drv = webdriver.Firefox(options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        drv = webdriver.Edge(options=options)
    drv.maximize_window()
    drv.implicitly_wait(10)
    yield drv
    logger.info(f"Terminating driver for browser: {browser}")
    drv.quit()


# TC_001: Adding a product to the cart
def test_add_product_to_cart(driver):
    logger.info("TC_001: Adding a product to the cart")
    logger.info("Opening the main page")
    driver.get(BASE_URL)
    logger.info("Navigating to the 'Books' category")
    driver.find_element(By.LINK_TEXT, "Books").click()
    logger.info("Waiting for the product list to load")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
    logger.info("Navigating to the first product page")
    driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
    logger.info("Waiting for the 'Add to cart' button")
    add_to_cart = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']"))
    )
    logger.info("Clicking the 'Add to cart' button")
    add_to_cart.click()
    logger.info("Waiting for the success notification")
    notification = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success"))
    )
    logger.info(f"Notification received: {notification.text}")
    assert "The product has been added to your shopping cart" in notification.text
    logger.info("TC_001: Test passed\n")


# TC_002: Removing a product from the cart
def test_remove_product_from_cart(driver):
    logger.info("TC_002: Removing a product from the cart")
    logger.info("Opening the main page")
    driver.get(BASE_URL)
    logger.info("Navigating to the 'Books' category")
    driver.find_element(By.LINK_TEXT, "Books").click()
    logger.info("Waiting for the product list")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
    logger.info("Opening the first product page")
    driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
    logger.info("Waiting for the 'Add to cart' button")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']")))
    logger.info("Clicking the 'Add to cart' button")
    driver.find_element(By.CSS_SELECTOR, "input[value='Add to cart']").click()
    logger.info("Waiting for the success notification")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success")))
    logger.info("Navigating to the cart")
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    logger.info("Selecting the product for removal")
    driver.find_element(By.NAME, "removefromcart").click()
    logger.info("Clicking the 'Update shopping cart' button")
    driver.find_element(By.NAME, "updatecart").click()
    logger.info("Waiting for the empty cart message")
    empty_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".order-summary-content"))
    )
    logger.info(f"Message received: {empty_message.text}")
    assert "Your Shopping Cart is empty!" in empty_message.text
    logger.info("TC_002: Test passed\n")


# TC_003: Changing the product quantity in the cart
def test_change_product_quantity(driver):
    logger.info("TC_003: Changing the product quantity in the cart")
    logger.info("Opening the main page")
    driver.get(BASE_URL)
    logger.info("Navigating to the 'Books' category")
    driver.find_element(By.LINK_TEXT, "Books").click()
    logger.info("Waiting for the product list")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
    logger.info("Opening the first product page")
    driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
    logger.info("Waiting for the 'Add to cart' button")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']")))
    logger.info("Clicking the 'Add to cart' button")
    driver.find_element(By.CSS_SELECTOR, "input[value='Add to cart']").click()
    logger.info("Waiting for the success notification")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success")))
    logger.info("Navigating to the cart")
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    logger.info("Finding the quantity field")
    qty_field = driver.find_element(By.CSS_SELECTOR, "input.qty-input")
    logger.info("Clearing and entering new quantity: 3")
    qty_field.clear()
    qty_field.send_keys("3")
    logger.info("Clicking the 'updatecart' button")
    driver.find_element(By.NAME, "updatecart").click()
    logger.info("Getting the updated quantity")
    updated_qty = driver.find_element(By.CSS_SELECTOR, "input.qty-input").get_attribute("value")
    logger.info(f"Updated quantity: {updated_qty}")
    assert updated_qty == "3"
    logger.info("TC_003: Test passed\n")


# TC_004: Checking the correct display of category pages
def test_category_pages(driver):
    logger.info("TC_004: Checking the correct display of category pages")
    driver.get(BASE_URL)
    categories = ["Books", "Apparel & Shoes", "Jewelry"]
    for category in categories:
        logger.info(f"Checking category: {category}")
        driver.get(BASE_URL)
        logger.info(f"Finding the link for category '{category}'")
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, category))
        )
        link.click()
        logger.info("Waiting for the page title to appear")
        header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-title"))
        )
        logger.info(f"Found title: {header.text}")
        assert category.lower() in header.text.lower(), f"Title '{header.text}' does not contain '{category}'"
        logger.info("Checking for products on the page")
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        logger.info(f"Found products: {len(products)}")
        assert len(products) > 0, f"No products found for category {category}."
    logger.info("TC_004: Test passed\n")


# TC_005: Placing an order (Guest Checkout)
def test_guest_checkout(driver):
    logger.info("TC_005: Placing an order (Guest Checkout)")
    driver.get(BASE_URL)
    logger.info("Navigating to the 'Books' category")
    driver.find_element(By.LINK_TEXT, "Books").click()
    logger.info("Waiting for the product list")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
    logger.info("Opening the first product page")
    driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
    logger.info("Waiting for the 'Add to cart' button")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']")))
    logger.info("Clicking the 'Add to cart' button")
    driver.find_element(By.CSS_SELECTOR, "input[value='Add to cart']").click()
    logger.info("Waiting for the success notification")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success")))
    logger.info("Navigating to the cart")
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    logger.info("Checking the 'I agree with the terms of service' checkbox")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "termsofservice"))).click()
    logger.info("Clicking the 'Checkout' button")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
    logger.info("Checking for the Guest Checkout button")
    try:
        guest_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.checkout-as-guest-button"))
        )
        logger.info("Guest Checkout button found. Clicking.")
        guest_button.click()
    except Exception:
        logger.info("Guest Checkout button not found, continuing with checkout")
    logger.info("Filling out the Billing Address form")
    billing_fields = {
        "BillingNewAddress_FirstName": "Test",
        "BillingNewAddress_LastName": "User",
        "BillingNewAddress_Email": "testuser@example.com",
        "BillingNewAddress_City": "New York",
        "BillingNewAddress_Address1": "123 Test Street",
        "BillingNewAddress_ZipPostalCode": "10001",
        "BillingNewAddress_PhoneNumber": "1234567890"
    }
    for field_id, value in billing_fields.items():
        logger.info(f"Filling out field {field_id} with value '{value}'")
        field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, field_id)))
        field.clear()
        field.send_keys(value)
    logger.info("Selecting country 'United States'")
    Select(driver.find_element(By.ID, "BillingNewAddress_CountryId")).select_by_visible_text("United States")
    logger.info("Clicking the 'New Address Next Step' button")
    driver.find_element(By.CSS_SELECTOR, "input.button-1.new-address-next-step-button").click()
    logger.info("Selecting shipping method: checking 'PickUpInStore'")
    pickup_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "PickUpInStore"))
    )
    if not pickup_checkbox.is_selected():
        pickup_checkbox.click()
    logger.info("Clicking the button to confirm the shipping method")
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.new-address-next-step-button[onclick='Shipping.save()']"))
    )
    continue_button.click()
    logger.info("Selecting payment method")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.payment-method-next-step-button"))
    ).click()
    logger.info("Entering payment information")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.payment-info-next-step-button"))
    ).click()
    logger.info("Confirming the order")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.confirm-order-next-step-button"))
    ).click()
    logger.info("Waiting for the order confirmation message")
    confirmation = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".section.order-completed"))
    )
    logger.info(f"Message received: {confirmation.text}")
    assert "Your order has been successfully processed!" in confirmation.text
    logger.info("TC_005: Test passed\n")


# TC_006: Sorting products by price
def test_sort_products_by_price(driver):
    logger.info("TC_006: Sorting products by price")
    driver.get(BASE_URL)
    logger.info("Navigating to the 'Computers' category")
    driver.find_element(By.LINK_TEXT, "Computers").click()
    tabs = ["Desktops", "Notebooks", "Accessories"]
    for tab in tabs:
        logger.info(f"Navigating to the '{tab}' tab")
        driver.find_element(By.LINK_TEXT, tab).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.page.category-page"))
        )
        logger.info("Waiting for the sort dropdown to appear")
        sort_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "products-orderby"))
        )
        select = Select(sort_select)
        logger.info("Selecting sort: 'Price: Low to High'")
        select.select_by_visible_text("Price: Low to High")
        logger.info("Waiting for the page to update")
        time.sleep(2)
        logger.info(f"Getting product prices for the {tab} tab")
        price_elements = driver.find_elements(By.CSS_SELECTOR, ".prices")
        prices = []
        for elem in price_elements:
            text = elem.text.strip().replace("$", "").replace("€", "").replace(",", "")
            try:
                price_val = float(text)
                prices.append(price_val)
                logger.info(f"Found price: {price_val}")
            except Exception as ex:
                logger.info(f"Error converting price: {ex}")
        logger.info(f"Checking that prices are sorted in ascending order for the {tab} tab")
        assert prices == sorted(prices), f"Prices are not sorted for {tab}: {prices}"
    logger.info("TC_006: Test passed\n")


# TC_007: Adding a product review (with prior login)
def test_add_product_review(driver):
    logger.info("TC_007: Adding a product review")
    driver.get(BASE_URL)
    logger.info("Logging in")
    login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
    )
    login_link.click()
    logger.info("Filling out the login form")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "Email"))
    ).send_keys("jim_finch@gmail.com")
    driver.find_element(By.ID, "Password").send_keys("qwerty")
    driver.find_element(By.CSS_SELECTOR, "input.button-1.login-button").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Log out"))
    )
    logger.info("Login successful")
    driver.get(BASE_URL)
    logger.info("Navigating to the 'Books' category")
    driver.find_element(By.LINK_TEXT, "Books").click()
    logger.info("Waiting for the product list")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item"))
    )
    logger.info("Opening the first product page")
    driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
    logger.info("Scrolling down to display the 'Add your review' link")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    logger.info("Checking for the 'Add your review' link")
    review_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add your review"))
    )
    review_link.click()
    logger.info("Filling out the review form")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "AddProductReview_Title"))
    ).send_keys("Great Product")
    driver.find_element(By.ID, "AddProductReview_ReviewText").send_keys("I really liked this product. It meets my expectations.")
    logger.info("Selecting a 5-star rating")
    driver.find_element(By.CSS_SELECTOR, "input[id^='addproductrating'][value='5']").click()
    logger.info("Clicking the 'Submit Review' button")
    driver.find_element(By.CSS_SELECTOR, "input.button-1.write-product-review-button").click()
    logger.info("Waiting for the success notification")
    notification = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".result"))
    )
    logger.info(f"Notification received: {notification.text}")
    assert "Product review is successfully added." in notification.text
    logger.info("TC_007: Test passed\n")


# TC_008: Boundary testing of the product quantity field
def test_quantity_boundary_values(driver):
    logger.info("TC_008: Boundary testing of the product quantity field")
    driver.get(BASE_URL)
    logger.info("Logging in")
    login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
    )
    login_link.click()
    logger.info("Filling out the login form")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "Email"))
    ).send_keys("jim_finch@gmail.com")
    driver.find_element(By.ID, "Password").send_keys("qwerty")
    driver.find_element(By.CSS_SELECTOR, "input.button-1.login-button").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Log out"))
    )
    logger.info("Login successful")
    logger.info("Adding a product to the cart")
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Books").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
    driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']")))
    driver.find_element(By.CSS_SELECTOR, "input[value='Add to cart']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success")))
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    
    for value in ["0", "-1", "100000000"]:
        logger.info(f"\nTesting boundary value: {value}")
        qty_field = driver.find_element(By.CSS_SELECTOR, "input.qty-input")
        qty_field.clear()
        qty_field.send_keys(value)
        logger.info("Clicking the 'updatecart' button")
        driver.find_element(By.NAME, "updatecart").click()
        time.sleep(2)
        try:
            empty_message = driver.find_element(By.CSS_SELECTOR, ".order-summary-content")
            if "Your Shopping Cart is empty!" in empty_message.text:
                logger.info(f"Cart is empty for value {value}. Re-adding the product.")
                driver.get(BASE_URL)
                driver.find_element(By.LINK_TEXT, "Books").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
                driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']")))
                driver.find_element(By.CSS_SELECTOR, "input[value='Add to cart']").click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success")))
                driver.find_element(By.LINK_TEXT, "Shopping cart").click()
                continue
        except Exception as e:
            logger.info(f"Could not determine cart state for value {value}: {e}")
        
        errors = driver.find_elements(By.CSS_SELECTOR, ".field-validation-error, .message-error")
        if errors:
            logger.info(f"Validation errors found for value {value}")
            assert any(e.is_displayed() for e in errors), f"Error not displayed for value {value}"
        else:
            updated_value = driver.find_element(By.CSS_SELECTOR, "input.qty-input").get_attribute("value")
            logger.info(f"Updated value: {updated_value} (expected not equal to {value})")
            assert updated_value != value, f"Value not corrected for {value}"
    logger.info("TC_008: Test passed\n")


# TC_009: Testing the performance of the checkout page
def test_checkout_page_performance(driver):
    logger.info("TC_009: Testing the performance of the checkout page")
    driver.get(BASE_URL)
    logger.info("Navigating to the 'Books' category")
    driver.find_element(By.LINK_TEXT, "Books").click()
    logger.info("Waiting for the product list")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
    logger.info("Opening the first product page")
    driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
    logger.info("Clicking the 'Add to cart' button")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']")))
    driver.find_element(By.CSS_SELECTOR, "input[value='Add to cart']").click()
    logger.info("Waiting for the success notification")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success")))
    logger.info("Navigating to the cart")
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    logger.info("Measuring the load time of the checkout page")
    start = time.time()
    logger.info("Checking the 'I agree with the terms of service' checkbox")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "termsofservice"))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
    logger.info("Checking for the Guest Checkout button")
    try:
        guest_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.checkout-as-guest-button"))
        )
        logger.info("Guest Checkout button found. Clicking.")
        guest_button.click()
    except Exception:
        logger.info("Guest Checkout button not found, continuing with checkout")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "BillingNewAddress_FirstName")))
    load_time = time.time() - start
    logger.info(f"Checkout page load time: {load_time:.2f} seconds")
    assert load_time < 5, f"Checkout page loaded in {load_time:.2f} seconds, which is too long."
    logger.info("TC_009: Test passed\n")


# TC_010: Regression testing of the checkout process
def test_regression_checkout(driver):
    logger.info("TC_010: Regression testing of the checkout process")
    driver.get(BASE_URL)
    logger.info("Navigating to the 'Books' category")
    driver.find_element(By.LINK_TEXT, "Books").click()
    logger.info("Waiting for the product list")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-item")))
    logger.info("Opening the first product page")
    driver.find_element(By.CSS_SELECTOR, ".product-item h2 a").click()
    logger.info("Clicking the 'Add to cart' button")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']")))
    driver.find_element(By.CSS_SELECTOR, "input[value='Add to cart']").click()
    logger.info("Waiting for the success notification")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success")))
    logger.info("Navigating to the cart")
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "termsofservice"))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
    logger.info("Checking for the Guest Checkout button")
    try:
        guest_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.checkout-as-guest-button"))
        )
        logger.info("Guest Checkout button found. Clicking.")
        guest_button.click()
    except Exception:
        logger.info("Guest Checkout button not found, continuing with checkout")
    logger.info("Filling out the Billing Address form")
    billing_fields = {
        "BillingNewAddress_FirstName": "Regression",
        "BillingNewAddress_LastName": "Tester",
        "BillingNewAddress_Email": "regression@example.com",
        "BillingNewAddress_City": "Los Angeles",
        "BillingNewAddress_Address1": "456 Regression Ave",
        "BillingNewAddress_ZipPostalCode": "90001",
        "BillingNewAddress_PhoneNumber": "0987654321"
    }
    for field_id, value in billing_fields.items():
        logger.info(f"Filling out field {field_id} with value '{value}'")
        field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, field_id)))
        field.clear()
        field.send_keys(value)
    logger.info("Selecting country 'United States'")
    Select(driver.find_element(By.ID, "BillingNewAddress_CountryId")).select_by_visible_text("United States")
    logger.info("Clicking the 'New Address Next Step' button")
    driver.find_element(By.CSS_SELECTOR, "input.button-1.new-address-next-step-button").click()
    logger.info("Selecting shipping method: checking 'PickUpInStore'")
    pickup_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "PickUpInStore"))
    )
    if not pickup_checkbox.is_selected():
        pickup_checkbox.click()
    logger.info("Clicking the button to confirm the shipping method")
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.new-address-next-step-button[onclick='Shipping.save()']"))
    )
    continue_button.click()
    logger.info("Selecting payment method")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.payment-method-next-step-button"))
    ).click()
    logger.info("Entering payment information")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.payment-info-next-step-button"))
    ).click()
    logger.info("Confirming the order")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button-1.confirm-order-next-step-button"))
    ).click()
    logger.info("Waiting for the order confirmation message")
    confirmation = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".section.order-completed"))
    )
    logger.info(f"Message received: {confirmation.text}")
    assert "Your order has been successfully processed!" in confirmation.text
    logger.info("TC_010: Test passed\n")
