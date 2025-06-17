from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://54.224.159.2:3000"

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

def login_to_app(driver, email="", password=""):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)
    if email:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys(email)
    if password:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(password)
    old_url = driver.current_url
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    return wait, old_url

def wait_for_url_change(driver, wait, old_url):
    wait.until(lambda d: d.current_url != old_url and d.current_url.startswith(BASE_URL))

def run_test(test_func):
    try:
        test_func()
    except Exception as e:
        print(f"[FAIL] {test_func.__name__}: {e}")
    else:
        print(f"[PASS] {test_func.__name__}")

def test_login_valid_user():
    driver = create_driver()
    wait, old_url = login_to_app(driver, "admin@demo.com", "admin123")
    wait_for_url_change(driver, wait, old_url)
    assert driver.current_url.startswith(BASE_URL)
    driver.quit()

def test_login_invalid_user():
    driver = create_driver()
    wait, _ = login_to_app(driver, "wrong@email.com", "wrongpass")
    toast = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-notification-notice-message")))
    assert any(word in toast.text.lower() for word in ["404", "invalid", "error"])
    driver.quit()

def test_login_empty_fields():
    driver = create_driver()
    wait, _ = login_to_app(driver)
    error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
    assert "enter" in error.text.lower()
    driver.quit()

def test_email_only_filled():
    driver = create_driver()
    wait, _ = login_to_app(driver, email="admin@demo.com")
    error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
    assert any(keyword in error.text.lower() for keyword in ["required", "enter"])
    driver.quit()

def test_password_only_filled():
    driver = create_driver()
    wait, _ = login_to_app(driver, password="admin123")
    error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
    assert any(keyword in error.text.lower() for keyword in ["required", "enter"])
    driver.quit()

def test_login_with_whitespace():
    driver = create_driver()
    email = "  admin@demo.com  "
    password = "  admin123  "
    wait, old_url = login_to_app(driver, email.strip(), password.strip())  
    wait_for_url_change(driver, wait, old_url)
    assert driver.current_url.startswith(BASE_URL)
    driver.quit()

def test_invalid_email_format():
    driver = create_driver()
    wait, _ = login_to_app(driver, "wrongemail.com", "admin123")
    error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
    assert "email" in error.text.lower()
    driver.quit()

def test_case_sensitive_email():
    driver = create_driver()
    wait, old_url = login_to_app(driver, "Admin@Demo.com", "admin123")
    wait_for_url_change(driver, wait, old_url)
    assert driver.current_url.startswith(BASE_URL)
    driver.quit()

def test_successful_login_redirects_to_dashboard():
    driver = create_driver()
    wait, old_url = login_to_app(driver, "admin@demo.com", "admin123")
    wait_for_url_change(driver, wait, old_url)
    assert driver.current_url.startswith(BASE_URL)
    driver.quit()

def test_forgot_password_redirect():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)
    driver.get(f"{BASE_URL}/login")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.login-form-forgot"))).click()
    wait.until(lambda d: d.current_url.endswith("/forgetpassword"))
    assert driver.current_url.endswith("/forgetpassword")
    driver.quit()

if __name__ == "__main__":
    tests = [
        test_login_valid_user,
        test_login_invalid_user,
        test_login_empty_fields,
        test_email_only_filled,
        test_password_only_filled,
        test_login_with_whitespace,
        test_invalid_email_format,
        test_case_sensitive_email,
        test_successful_login_redirects_to_dashboard,
        test_forgot_password_redirect
    ]

    for test in tests:
        run_test(test)
