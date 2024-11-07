from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

courses = ['01 - COMPUTER (COMPUTER SCIENCE & ENGINEERING)', '02 - COMPUTER ENGINEERING', '03 - INSTRUMENTATION AND CONTROL(APPLIED INSTRUMENTATION)', '04 - ELECTRONICS AND COMMUNICATION ENGINEERING', '05 - ELECTRONICS AND COMMUNICATION (COMMUNICATION SYSTEM ENGINEERING)', '06 - ELECTRONICS AND COMMUNICATION (COMMUNICATION ENGINEERING)', '07 - ELECTRICAL ENGINEERING', '08 - MECHANICAL (CAD/CAM)', '09 - MECHANICAL (MACHINE DESIGN)', '10 - MECHANICAL (CRYOGENIC ENGINEERING)', '11 - MECHANICAL (I.C.ENGINE & AUTOMOBILE)', '12 - CIVIL ( WATER RESOURCES MANAGEMENT)', '13 - CIVIL (TRANSPORTATION ENGINEERING)', '14 - CIVIL (CONSTRUCTION ENGINEERING AND MANAGEMENT)', '15 - CIVIL (CASAD)', '16 - CHEMICAL ENGINEERING (COMPUTER AIDED PROCESS DESIGN)', '17 - ENVIRONMENTAL ENGINEERING', '18 - ENVIRONMENTAL MANAGEMENT', '19 - CIVIL (TRANSPORTATION SYSTEM ENGINEERING)', '20 - CIVIL (STRUCTURAL ENGINEERING)', '21 - MECHANICAL (THERMAL ENGINEERING)', '22 - ELECTRONICS AND COMMUNICATION (DIGITAL COMMUNICATIONS)', '23 - INFORMATION TECHNOLOGY', '24 - PLASTIC ENGINEERING', '25 - TEXTILE ENGINEERING', '26 - ELECTRONICS AND COMMUNICATION (SIGNAL PROCESSING AND VLSI TECHNOLOGY)', '27 - ELECTRONICS AND COMMUNICATION (WIRELESS COMMUNICATION SYSTEMS AND NETWORKS)', '28 - MECHANICAL (PRODUCTION ENGINEERING)', '29 - POWER ELECTRONICS', '30 - CHEMICAL ENGINEERING', '31 - BIO MEDICAL ENGINEERING', '32 - CIVIL (COMPUTER AIDED STRUCTURAL ANALYSIS)', '33 - CIVIL (WATER RESOURCE ENGINEERING)', '34 - MECHANICAL (THERMAL SCIENCE)', '35 - MECHANICAL (AUTOMOBILE ENGINEERING)', '36 - ME ELECTRICAL (AUTOMATION AND CONTROL POWER SYSTEM)', '37 - ELECTRICAL (POWER SYSTEM ENGINEERING)', '38 - COMPUTER (COMPUTER SCIENCE & TECHNOLOGY)', '39 - MECHANICAL (ENERGY ENGINEERING)', '40 - RUBBER ENGINEERING', '41 - ELECTRONICS AND COMMUNICATION (SIGNAL PROCESSING & COMMUNICATION)', '42 - ELECTRONICS AND COMMUNICATION (VLSI SYSTEM DESIGN)', '43 - CIVIL (GEOTECHNICAL ENGINEERING)', '44 - ELECTRONICS AND COMMUNICATION (WIRELESS COMMUNICATION TECHNOLOGY)', '45 - ELECTRICAL (POWER ELECTRONICS & ELECTRICAL DRIVES)', '46 - MECHANICAL (INDUSTRIAL ENGINEERING)', '47 - MECHATRONICS', '48 - TOWN AND COUNTRY PLANNING', '49 - CONSTRUCTION MANAGEMENT', '50 - ADVANCED MANUFACTURING SYSTEMS', '51 - COMPUTER ENGINEERING (IT SYSTEMS AND NETWORK SECURITY)', '52 - ELECTRONICS AND COMMUNICATION (VLSI & EMBEDDED SYSTEMS DESIGN)', '53 - COMPUTER ENGINEERING (WIRELESS & MOBILE COMPUTING)', '54 - ELECTRONICS AND COMMUNICATION (EMBEDDED SYSTEM)', '55 - COMPUTER ENGINEERING (HIGH PERFORMANCE COMPUTING)', '56 - COMPUTER ENGINEERING (SYSTEMS AND NETWORK SECURITY)', '59 - CYBER SECURITY', '60 - ELECTRONICS AND COMMUNICATION ENGINEERING (MOBILE COMMUNICATION AND NETWORK TECHNOLOGY)', '61 - EC (VLSI AND EMBEDDED SYSTEMS)', '62 - INTERNET OF THINGS', '63 - VLSI DESIGN', '64 - ELECTRIC VEHICLE TECHNOLOGY', '65 - CIVIL ENGINEERING', '66 - ADVANCED MANUFACTURING TECHNOLOGY', '67 - APPLIED INSTRUMENTATION', '68 - CAD/CAM', '69 - CIVIL ENGINEERING(TRANSPORTATION ENGINEERING)', '70 - COMPUTER AIDED DESIGN AND MANUFACTURE', '71 - COMPUTER AIDED DESIGN MANUFACTURE AND ENGINEERING', '72 - COMPUTER AIDED PROCESS DESIGN', '73 - COMPUTER ENGINEERING(SOFTWARE ENGINEERING)', '74 - CRYOGENIC ENGINEERING', '75 - ENERGY ENGINEERING', '76 - GEOTECHNICAL ENGINEERING', '77 - INFORMATION TECHNOLOGY(INFORMATION AND CYBER WARFARE)', '78 - MACHINE DESIGN', '79 - MECHANICAL ENGINEERING', '80 - MECHANICAL(I.C. ENGINE AND AUTOMOBILE ENGINEERING)', '81 - MECHANICAL ENGINEERING(CAD/CAM)', '82 - MECHANICAL ENGINEERING(PRODUCTION)', '83 - MECHANICAL ENGINEERING(THERMAL ENGINEERING)', '84 - PLASTICS ENGINEERING', '85 - POWER ELECTRONICS AND ELECTRICAL DRIVES', '86 - POWER SYSTEMS', '87 - PRODUCTION ENGINEERING', '88 - RUBBER TECHNOLOGY', '89 - STRUCTURAL ENGINEERING', '94 - ME (MECH) ARMAMENT ENGINEERING', '95 - ARTIFICIAL INTELLIGENCE AND DATA SCIENCE']
years = ['2024-25', '2023-24', '2022-23', '2021-22', '2019-20', '2018-19', '2017-18', '2014-15', '2013-14', '2012-13', '2011-12', '2010-11', '2009-10']

# Set up Chrome options and ChromeDriver service
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/home/manav1011/Downloads/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the webpage
driver.get("https://syllabus.gtu.ac.in/Syllabus.aspx?tp=ME")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddcourse")))

data = {}

for course in courses:
    print(f"Now fetching course {course}")
    data[course] = {}
    second_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlbrcode")))
    Select(second_dropdown).select_by_visible_text(course)
    
    # Define the years you want to iterate over    
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
                            // Select the table by ID
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
                            if(single_obj[headers[count]] == undefined){
                                single_obj[headers[count]] = textContent   
                            }else{
                            single_obj[`${headers[count]}2`] =textContent
                            }
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

driver.quit()
with open("ME.json", "w") as json_file:
    json.dump(data, json_file, indent=4) 