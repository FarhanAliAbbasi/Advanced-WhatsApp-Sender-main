from PyQt5.QtCore import pyqtSignal, QThread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from subprocess import CREATE_NO_WINDOW
import time
import os
import re
from appLog import log

class MapsWeb(QThread):
    progress = pyqtSignal(str)
    lead_found = pyqtSignal(dict)
    finished = pyqtSignal(str)

    def __init__(self, query, parent=None):
        super(MapsWeb, self).__init__(parent)
        self.query = query
        self.isRunning = True
        self.driver = None
        self.service = Service()
        self.service.creation_flags = CREATE_NO_WINDOW

    def extract_phone_from_text(self, text):
        # Match standard phone number patterns (with spaces, hyphens, country code, etc.)
        matches = re.findall(r'(?:\+?\d{1,3}[-\s\.\(\)]?)?\(?\d{3,4}\)?[-\s\.\(\)]?\d{3,4}[-\s\.\(\)]?\d{3,4}', text)
        for match in matches:
            clean = "".join(filter(str.isdigit, match))
            if 9 <= len(clean) <= 13:
                return match
        return None

    def init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        # Reuse the same profile if possible, or a separate one for maps
        user_data = os.path.abspath('./temp/profile_maps')
        if not os.path.exists(user_data):
            os.makedirs(user_data)
        options.add_argument(f"--user-data-dir={user_data}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.page_load_strategy = 'eager'
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.driver = webdriver.Chrome(options=options, service=self.service)
        self.driver.set_window_size(1024, 768)
        self.driver.set_page_load_timeout(15)

    def run(self):
        try:
            self.progress.emit(f"Searching for: {self.query}")
            self.init_driver()
            try:
                # Go to generic maps first
                self.driver.get("https://www.google.com/maps")
            except Exception as e:
                pass
            
            time.sleep(3)
            
            # Type search query into the box to force a true search
            try:
                search_box = self.driver.find_element(By.ID, "searchboxinput")
                search_box.clear()
                search_box.send_keys(self.query)
                search_box.send_keys(Keys.RETURN)
            except Exception as e:
                self.progress.emit("Warning: Search box not found, trying URL fallback...")
                import urllib.parse
                encoded_query = urllib.parse.quote_plus(self.query)
                try:
                    self.driver.get(f"https://www.google.com/maps/search/{encoded_query}")
                except:
                    pass
            
            time.sleep(5)
            found_leads = set()
            
            self.progress.emit("Ready. Please search and click on businesses manually...")
            found_leads = set()
            
            while self.isRunning:
                time.sleep(1.5)
                
                try:
                    # Look for the business title (h1 is typically used for the business name in the details pane)
                    h1_elements = self.driver.find_elements(By.XPATH, '//h1')
                    if not h1_elements:
                        continue
                        
                    name = "N/A"
                    for h1 in h1_elements:
                        if h1.text and len(h1.text) > 1:
                            name = h1.text
                            break
                            
                    if name == "N/A" or name in found_leads:
                        continue
                        
                    # Now look for the phone number in the details pane
                    phone = "N/A"
                    phone_selectors = [
                        '//button[contains(@aria-label, "Phone:")]',
                        '//button[contains(@data-item-id, "phone")]',
                        '//a[contains(@href, "tel:")]',
                        '//div[contains(@aria-label, "Phone:")]'
                    ]
                    
                    for selector in phone_selectors:
                        try:
                            phone_el = self.driver.find_element(By.XPATH, selector)
                            phone_text = phone_el.get_attribute("aria-label") or phone_el.text
                            if phone_text:
                                phone_text = phone_text.replace("Phone: ", "").strip()
                                # Basic check for phone digits
                                if any(char.isdigit() for char in phone_text):
                                    phone = phone_text
                                    break
                        except:
                            continue
                            
                    # If phone is still N/A, try searching the left search results list
                    if phone == "N/A":
                        try:
                            # Search by aria-label first (most reliable for maps search items)
                            card_elements = self.driver.find_elements(By.XPATH, f'//a[contains(@aria-label, "{name}")]')
                            if not card_elements:
                                card_elements = self.driver.find_elements(By.XPATH, f'//*[contains(text(), "{name}")]')
                            
                            for card in card_elements:
                                card_text = card.text
                                if card_text:
                                    extracted = self.extract_phone_from_text(card_text)
                                    if extracted:
                                        phone = extracted
                                        break
                        except Exception as e:
                            log.debug(f"Error parsing left pane card: {e}")
                            
                    if phone != "N/A":
                        clean_phone = "".join(filter(str.isdigit, phone))
                        if len(clean_phone) >= 7:
                            lead = {"name": name, "phone": clean_phone}
                            self.lead_found.emit(lead)
                            self.progress.emit(f"SAVED: {name} -> {clean_phone}")
                            found_leads.add(name)
                    else:
                        # We saw the name, but no phone. We'll add it to found_leads so we don't spam
                        # the check, but we won't emit it.
                        found_leads.add(name)
                        
                except Exception as e:
                    continue
                    
            self.finished.emit(f"Extraction finished. Total leads: {len(found_leads)}")
            
        except Exception as e:
            error_msg = str(e).split('\n')[0]
            self.progress.emit(f"ERROR: {error_msg}")
            log.debug(f"Maps extraction error: {e}")
        finally:
            if hasattr(self, 'driver'):
                try:
                    self.driver.quit()
                except:
                    pass

    def stop(self):
        self.isRunning = False
