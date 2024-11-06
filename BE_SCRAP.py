from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

# Set up Chrome options and ChromeDriver service
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/home/manav1011/Downloads/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the webpage
driver.get("https://syllabus.gtu.ac.in/Syllabus.aspx?tp=BE")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddcourse")))

data = {}
courses = ['01 - AERONAUTICAL ENGINEERING', '02 - AUTOMOBILE ENGINEERING', '03 - BIO-MEDICAL ENGINEERING', '04 - BIO-TECHNOLOGY', '05 - CHEMICAL ENGINEERING', '06 - CIVIL ENGINEERING', '07 - COMPUTER ENGINEERING', '08 - ELECTRICAL & ELECTRONICS ENGINEERING', '09 - ELECTRICAL ENGINEERING', '10 - ELECTRONICS ENGINEERING', '11 - ELECTRONICS & COMMUNICATION ENGINEERING', '12 - ELECTRONICS & TELECOMMUNICATION ENGINEERING', '13 - ENVIRONMENTAL ENGINEERING', '14 - FOOD PROCESSING TECHNOLOGY', '15 - INDUSTRIAL ENGINEERING', '16 - INFORMATION TECHNOLOGY', '17 - INSTRUMENTATION & CONTROL ENGINEERING', '18 - MARINE ENGINEERING', '19 - MECHANICAL ENGINEERING', '20 - MECHATRONICS ENGINEERING', '21 - METALLURGY ENGINEERING', '22 - MINING ENGINEERING', '23 - PLASTIC TECHNOLOGY', '24 - POWER ELECTRONICS', '25 - PRODUCTION ENGINEERING', '26 - RUBBER TECHNOLOGY', '28 - TEXTILE PROCESSING', '29 - TEXTILE TECHNOLOGY', '31 - COMPUTER SCIENCE & ENGINEERING', '32 - INFORMATION & COMMUNICATION TECHNOLOGY', '34 - MANUFACTURING ENGINEERING', '35 - ENVIRONMENTAL SCIENCE & TECHNOLOGY', '36 - CHEMICAL TECHNOLOGY', '37 - ENVIRONMENTAL SCIENCE AND ENGINEERING', '39 - NANO TECHNOLOGY', '40 - CIVIL & INFRASTRUCTURE ENGINEERING', '41 - ROBOTICS AND AUTOMATION', '42 - COMPUTER SCIENCE & ENGINEERING (ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)', '43 - ARTIFICIAL INTELLIGENCE AND DATA SCIENCE', '44 - CHEMICAL ENGINEERING (GREEN TECHNOLOGY & SUSTAINABILITY ENGINEERING)', '45 - COMPUTER SCIENCE & ENGINEERING (INTERNET OF THINGS AND CYBER SECURITY INCLUDING BLOCK CHAIN TECHNOLOGY)', '46 - COMPUTER SCIENCE & ENGINEERING (DATA SCIENCE)', '47 - ELECTRONICS & INSTRUMENTATION ENGINEERING', '48 - COMPUTER SCIENCE & ENGINEERING (CYBER SECURITY)', '49 - COMPUTER SCIENCE & DESIGN', '50 - SMART & SUSTAINABLE ENERGY', '51 - FOOD ENGINEERING & TECHNOLOGY', '52 - ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING', '53 - PLASTICS ENGINEERING', '54 - ELECTRONICS AND COMMUNICATION (COMMUNICATION SYSTEM ENGINEERING)', '89 - MECHANICAL ENGINEERING', 'AA - MINOR/HONORS -INDUSTRIAL PROCESS SAFETY', 'AB - MINOR/HONORS -WASTE TECHNOLOGY', 'AC - MINOR/HONORS -CONSTRUCTION TECHNOLOGY', 'AD - MINOR/HONORS -NEXT GENERATION SMART VILLAGE', 'AE - MINOR/HONORS -INFRASTRUCTURE ENGINEERING', 'AF - MINOR/HONORS -SMART CITIES', 'AG - MINOR/HONORS -ARTIFICIAL INTELLIGENCE & MACHINE LEARNING', 'AH - MINOR/HONORS -CYBER SECURITY', 'AI - MINOR/HONORS -INTERNET OF THINGS', 'AJ - MINOR/HONORS - SOLAR ENERGY SYSTEMS', 'AK - MINOR/HONORS -ELECTRICAL AND COMPUTER', 'AL - MINOR/HONORS -ELECTRIC VEHICLES', 'AM - MINOR/HONORS -CONTROL SYSTEMS AND SENSORS TECHNOLOGY', 'AN - MINOR/HONORS -3 D PRINTING', 'AO - MINOR/HONORS -ROBOTICS', 'AP - MINOR/HONORS -ENERGY ENGINEERING', 'AQ - MINOR/HONORS - GLOBAL CITIZENSHIP PERSONALITY DEVELOPMENT', 'AR - MINOR/HONOURS-INDUSTRIAL BASED NON DESTRUCTIVE TECHNIQUES AND PRACTICES', 'AS - MINOR/HONOURS-GREEN TECHNOLOGY AND SUSTAINABILITY ENGINEERING', 'AT - MINOR/HONOURS-DATA SCIENCE', 'AU - MINOR/HONOURS-FORENSIC STRUCTURAL ENGINEERING', 'AV - MINOR/HONOURS-COMPUTER AIDED CIVIL ENGINEERING PROCESSES', 'NA - ARMY', 'NB - AIR FORCE', 'NC - NAVY']
years = ['2008-09', '2013-14', '2014-15','2015-16','2016-17','2017-18','2018-19','2020-21','2021-22','2022-23','2023-24','2024','2024-25']

for course in courses:
    print(f"Now fetching course {course}")
    data[course] = {}
    second_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlbrcode")))
    Select(second_dropdown).select_by_visible_text(course)
    
    # Define the years you want to iterate over
    years = ['2008-09', '2013-14', '2014-15','2015-16','2016-17','2017-18','2018-19','2020-21','2021-22','2022-23','2023-24','2024','2024-25']
    
    for year in years:
        print(f"Now fetching year {year}")
        third_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddl_effFrom")))
        Select(third_dropdown).select_by_visible_text(year)
        
        # Click the search button
        search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btn_search")))
        search_button.click()
        
        try:
            # Wait for the element with ID 'GridViewToCategory' to appear
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, "GridViewToCategory"))
            )
            
            # Execute JavaScript to retrieve 'data' variable from the page if the element exists
            script = """
                var table = $('#GridViewToCategory');
            // Find the first <tr> inside the <tbody>
            var firstRow = table.find('tbody').first().find('tr').first();
            var headers = []

            // Extract the text of every <th> element inside the first <tr>
            firstRow.children('th').each(function() {
                headers.push($(this).text().trim())
            });

            // Find all the <tr> elements starting from the second row
            var rows = table.find('tbody').first().find('tr').not(':first');

            count = 0
            var data = []
            var single_obj = {}
            rows.each(function(rowIndex) {
                $(this).children('td').each(function(cellIndex) {
                    // Extract the direct text content from the <td> (ignoring nested tags)
                    var textContent = $(this).text().replace(/\s+/g, ' ').trim(); // Clean the text (remove excessive spaces)
                    if(textContent.length > 0){
                        if(count<16){
                            single_obj[headers[count]] = textContent
                        }else{
                            var parts = textContent.split(':');
                            var key = parts[0].trim(); // Key before the colon
                            var value = parts[1].trim(); // Value after the colon
                            single_obj[key] = value
                        }
                    count++;
                    if(count == 25){
                            count= 0;
                            data.push(single_obj)
                            single_obj = {}
                    }
                    }
                });
            });

            return data
            """
            
            output = driver.execute_script(script)
            data[course][year] = output

        except Exception as e:
            # Handle the case where 'GridViewToCategory' is not found within 10 seconds
            print(e)
print('here')
driver.quit()
with open("BE.json", "w") as json_file:
    json.dump(data, json_file, indent=4) 