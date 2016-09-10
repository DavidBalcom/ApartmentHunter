## Synopsis

This is a script to search craigslist for apartments in your desired area and price range. Run the script periodically, and it will email you when new apartments show up. There is also a webpage with a map to make it easier to save the coordinates your desired areas. The script works by getting the lati

## Set Up

1) open mapStandalone.html in a browser, and define your areas using the rectangle. Click the save area button, and paste the output into locations.config.

2) Edit the settings.py file with your price range, email address, and Craigslist subdomain. Some Craigslist  subdomains have other regions inside them. If that's the case for yours, edit the 'url_part' variable, otherwise leave it empty. 

3) Set the script_frequency variable to however frequently you want the script to run, in minutes. Create a cron job for this script to run with the same frequency, and it should work...

except that I haven't posted the email library, so you'll need to write your own email library for now. Sorry!

