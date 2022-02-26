import requests 
from bs4 import BeautifulSoup
import csv

keyword = 'solar'
location = 'india'

def make_request(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    return soup


def extract_data():
    csvFile = open('talent.csv', mode='w', encoding='utf-8')
    page = 1
    i = 1
    try:
        writer = csv.writer(csvFile)
        #columns names
        writer.writerow(('Sr','Job Title', 'Company Name','Salary','Location','Job Url'))
        while True:
            url = f'https://in.talent.com/jobs?k={keyword}&p={page}'
            soup = make_request(url)
            div_tag = soup.find('div' , id='nv-jobs')
            jobs_list = div_tag.find_all('div' , class_='card card__job')
            #extracting data
            if(len(jobs_list)!=0):
                for job in jobs_list:
                    job_title = "Not Available"
                    company_name = "Not Available"
                    location = "Not Available"
                    salary = "Not Available"
                    job_url = " "
                    sr_no = i
                    id = job['data-id']
                    title_tag = job.find('h2' , class_='card__job-title')
                    company_name_tag = job.find('div', class_='card__job-empname-label')
                    locations_tag = job.find('div' , class_='card__job-location')
                    salary_tag = job.find('div' ,class_='card__job-badge-wrap card__job-badge-salary' )
                    job_url = "https://in.talent.com/view?id="+id
                    if(title_tag != None):
                        job_title = title_tag.text.strip()
                    if(company_name_tag != None):
                        company_name = company_name_tag.text.strip()
                    if(locations_tag != None):
                        location = locations_tag.text.strip()
                    if(salary_tag != None):
                        salary = salary_tag.text.strip()

                    print ("Sr No: "+ str(sr_no) )
                    print("Job Url: " + job_url )
                    print("Title: "+ job_title)
                    print("Company Name: "+ company_name)
                    print("Locations: "+ location)
                    print("Salary: "+salary)
                    print(" ")
                    writer.writerow((sr_no,job_title,company_name,salary,location,job_url))
                    i = i+1
                    
                page = page+1
            else:
                break
    except Exception as e:
        print(e)
        
    finally:
        csvFile.close()

        
def main():
    extract_data()
    
    
if __name__ == '__main__':
    main()