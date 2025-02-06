from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time


def send_file_to_whatsapp(recipients, file_path):
    """Automates sending a file to multiple WhatsApp groups or individuals."""

    # Initialize WebDriver
    driver = webdriver.Chrome()

    try:
        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com")
        input("Scan the QR code and press Enter to continue...")

        for recipient in recipients:
            try:
                # Locate the search box and search for the recipient
                search_box = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-autocomplete='list']"))
                )
                search_box.clear()
                search_box.send_keys(recipient)

                # Wait for the chat to load and click it
                chat = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, f"//span[@title='{recipient}']"))
                )
                chat.click()

                # Locate the attach button and click it
                attach_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-icon='plus']"))
                )
                attach_button.click()

                # Locate the document upload button and click it
                document_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
                )
                document_button.send_keys(file_path)

                # Wait for a few seconds to ensure the file is uploaded
                time.sleep(3)

                # Locate the send button and click it
                send_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-icon='send']"))
                )

                send_button.click()
                print(f"File sent to {recipient} successfully.")
            except Exception as e:
                print(f"Failed to send file to {recipient}: {e}")
            finally:
                time.sleep(10)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the browser after the operation
        driver.quit()


# Main logic
if __name__ == "__main__":
    # Get recipient names and file path
    recipients = ["News & Cartoons",
                  "an International papers Israeli/other",
                  "רוטר .פוליטיקה, אקטואליה ועיתונים",
                  "רוטר-חברים 2.עיתונים",
                  "פסטל אזור חופשי.pastel"
                  ]  # Fixed list of recipients
    file_path = input("Enter the location file path (e.g., C:/Users/USER/Desktop/daily news.pdf)")  # Fixed file path

    if Path(file_path).is_file():
        # Send the file to the specified recipients
        if recipients and file_path:
            send_file_to_whatsapp(recipients, file_path)
        else:
            print("Recipients and file path cannot be empty.")
    else:
        print("File specified is invalid")