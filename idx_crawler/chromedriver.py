from get_chrome_driver import GetChromeDriver

# Main function
if __name__ == "__main__":
    get_driver = GetChromeDriver()

    # Print the stable version
    print(f"Chrome version: {get_driver.stable_version()}")

    # Print the stable version download link
    print(f"Download Chrome Bot from url: {get_driver.stable_version_url()}")

    # Download driver
    get_driver.download_stable_version(extract=True)
    print("Chrome Bot is already to use")