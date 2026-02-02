import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ==========================================
# 👇 PASTE YOUR STREAMLIT URLS HERE 👇
# ==========================================
URL_LIST = [
    "https://your-app-one.streamlit.app",
    "https://your-app-two.streamlit.app",
    "https://your-cool-project.streamlit.app"
]
# ==========================================

def process_url(url):
    print(f"🚀 [START] Checking: {url}")
    
    # Configure Chrome for GitHub Servers (Headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        # Wait 5 seconds for the page to load the "Yes" button if it exists
        time.sleep(5) 

        # Look for the specific text
        xpath = "//*[contains(text(), 'Yes, get this app back up!')]"
        buttons = driver.find_elements(By.XPATH, xpath)
        
        if buttons:
            print(f"💤 [SLEEPING] '{url}' is asleep. Clicking wake up button...")
            buttons[0].click()
            
            # Wait 3 minutes (180 seconds) for this specific app to reload
            print(f"⏳ [WAITING] 3 minutes for '{url}' to boot up...")
            time.sleep(180)
            
            # Optional: Check title after wait
            print(f"✅ [AWAKE] '{url}' should be up now. Page title: {driver.title}")
        else:
            print(f"⚡ [ACTIVE] '{url}' is already running. No action needed.")

    except Exception as e:
        print(f"❌ [ERROR] Could not check '{url}': {e}")
    
    finally:
        driver.quit()

def run_all_checks():
    print(f"--- Starting checks for {len(URL_LIST)} apps ---")
    
    # Run up to 4 browsers in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_url, URL_LIST)
        
    print("--- All checks finished ---")

if __name__ == "__main__":
    run_all_checks()