### Project implementation process
* Define the features and functionalities of web application (described in MDS+AI.canvas) - ==**DONE**==
* Set up Python Flask development environment on local machine
	* ==**Flask main tutorials**==
		* https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
		* https://coda.io/d/_dfQbJFuP6kM/Flask_suQGV
		* https://coda.io/d/_dzY0bThqlVT/Flask-2_surR-
	* Is needed to use in apps core code:
		* [Store configurations of the application in separate Python file](https://coda.io/d/_dfQbJFuP6kM#Flask-objects-and-attributes_tuwAp/r2&view=modal): for more complex applications, it's often beneficial to store configuration in a separate Python file ==outside of application's package and not included in version control. This allows for easier management and deployment of your application==.It's important to load the configuration early in application's lifecycle to ensure that all extensions and parts of application have access to the configuration values when they start up
			* Use [`from_pyfile`](https://coda.io/d/_dfQbJFuP6kM#Flask-methods-and-functions_tuiZc/r1&view=modal) method to load `configurations.py` file into Flask project 
		* Apps structure
			* Use [Flask-Classy routing extension](https://coda.io/d/_dfQbJFuP6kM/Flask_suQGV#_luBc9) in structurizing apps routes ==(create one class  - one routes branch)==
			* Homepage implementation 
			* Login implementation with cookies
				* User authentication management
					* Implement user authentication to secure the application
                        * Where shold be user data stored
						* Is it needed to be stored in special e.g. MySQL database 
						* If yes, how to connect that with apps backend structure using SQLAlchemy 
						* Use this [guide](https://coda.io/d/_dzY0bThqlVT/Flask-2_surR-#_luG0F) to properly implement connection code-SQLAlchemy-MySQL database
			* Personal page implementation
				* Develop subscription management features for users - to subscribe/unsubscribe to daily emails
					* This function must be availible for user on an ongoing basis from its personal page
					* Provide options for users to manage their preferences and account settings
			* Uploading files implementation: [`request.files`](https://coda.io/d/_dfQbJFuP6kM#Flask-objects-and-attributes_tuwAp/r1&view=modal) gives abbility to upload files to the server for for further work. Add all security applets
	            * Store the uploaded PDF files securely on the server or use cloud storage (e.g., AWS S3, Google Cloud Storage)
                * Explore the ability not to store downloaded files on the server
			* Preliminar summaries menu page implementation
				* Which loads after uploading text-file
				* Contains separated chapters of file with short summaries of every chapter
				* Every chapter can be chosen or not chosen for mailing by user
				* Add button to choose or unchoose all chapters   
		* Provide security 
			* [Secure client-side sessions in Flask app](https://coda.io/d/_dfQbJFuP6kM#Security-ensuring-in-Flask_tuIaO/r2&view=modal)
			* [Use HTTPS protocol in server connection](https://coda.io/d/_dfQbJFuP6kM#Security-ensuring-in-Flask_tuIaO/r5&view=modal)
			* Explore [this info block](https://web.dev/explore/secure) to provide security comprehensively  
* Web applications UX/UI creation
	* Initialize a new project and set up the necessary dependencies
		* Get the guide of this process
	* Develop the frontend for user interaction, including the upload form
		* Get the guide of this process
		* Consider the possibility of [SQLAlchemy](https://shantdanielyan.slite.com/api/s/F3-fcjCrhd6iAQ/SQLAlchemy) usage in interfacing frontend with backend databases
			* If it is needed for the project, create Coda page for SQLAlchemy and take info from these sources: https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/; https://www.datacamp.com/tutorial/sqlalchemy-tutorial-examples
		* Plan the user interface and user experience (is in MDS+AI.canvas) - ==**DONE**==
		* Use design software like Figma for creating high-fidelity mockups and prototypes
* AI API for text documents summarization
	* OpenAI API is best suited for this task
	* This approach involves several steps
		* Reading the PDF content using Python modules
			* Use the `fitz` library to read the PDF file and extract its text content. The `fitz.open(filename)` method opens the PDF file, and iterating through each page with `pdf_file[page_num].get_text()` extracts the text
			* The fitz library, also known as PyMuPDF, is a set of Python bindings for the MuPDF library. It provides a way to interact with and manipulate various document formats, including PDF, XPS, OpenXPS, CBZ, CBR, FB2, and EPUB, within Python
			* The library allows to perform tasks such as opening and accessing documents, working with outlines (bookmarks), handling pages, extracting text and images, and rendering pages into raster or vector images
			* Install PyMuPDF library from command line: `pip install PyMuPDF openai` - **==DONE==**
		* Breaking down the text into manageable chunks 
			* Every OpenAI API call is treated separately - there is no “memory function”. That means that it won't be possible to store whole PDF file in one query for AI 
			* That is why we split extracted text into smaller chunks using the custom `split_text` function. This function divides the text into paragraphs containing approximately 5000 characters each, making it easier to process and summarize
		* Using the GPT-3 model to generate summaries for each chunk
			* Custom `gpt3_completion` function will send a request to the OpenAI GPT-3 API with a prompt to summarize the text chunk. The response from the API is the generated summary
			* It will generate separate summaries to every text chunks 
			* **OpenAI API** integration guide
				* Go to the OpenAI website and sign up for an API key (keep API key secure)
				* Follow the instructions to get your API key and access token
				* Select a programming language and framework for your web application. ==It is Python Flask==
				* Install the OpenAI Python SDK using command `pip install openai` - ==**DONE**==
				* Enter personal OpenAI API key in code (its place is indicated in code example below)
		* Storing summaries 
			* Here is needed to organize storage of every chunks summary separately in lists 
				* ==But consider the possibility of dictionary using instead of lists. **Conduct a comparative analysis**==
			* Also is needed to generate summaries to already generated summaries for presentation to user before subscription
				* App must show to user ==on the web interface== the mailing plan, a mailing schedule - with the name of every theme and three main thesis of every chapter (subscription message)
			* Connect the PDF parsing and summarization logic with web application's file upload functionality
		* Test application to ensure that the summarization process works correctly for different PDF files and chapters
```
import fitz
import openai
from nltk.tokenize import sent_tokenize
from io import StringIO

# Function to read PDF content
def read_pdf(filename):
    context = ""
    with fitz.open(filename) as pdf_file:
        for page_num in range(pdf_file.page_count):
            page = pdf_file[page_num]
            page_text = page.get_text()
            context += page_text
    return context

# Function to split text into chunks
def split_text(text, chunk_size=5000):
    chunks = [] 
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        if current_size + len(sentence) < chunk_size:
            current_chunk.write(sentence)
            current_size += len(sentence)
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = len(sentence)
    if current_chunk.getvalue():
        chunks.append(current_chunk.getvalue())
    return chunks

# Function to generate summary using GPT-3
def gpt3_completion(prompt, engine='text-davinci-003', temp=0.5, top_p=0.3, tokens=1000):
    prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temp,
            top_p=top_p,
            max_tokens=tokens
        )
        return response.choices[0].text.strip()
    except Exception as oops:
        return "GPT-3 error: %s" % oops

# Main function to summarize the PDF
def summarize_pdf(filename):
    # Read the PDF content
    pdf_content = read_pdf(filename)
    
    # Split the content into chunks
    text_chunks = split_text(pdf_content)
    
    # Generate summaries for each chunk
    summaries = []
    for chunk in text_chunks:
        prompt = f"Summarize the following text:\n\n{chunk}"
        summary = gpt3_completion(prompt)
        summaries.append(summary)
    
    # add snippet to store all generated summaries of PDF

# Example usage. Also need to customize
if __name__ == "__main__":
    openai.api_key = 'your_openai_api_key_here'  # enter here my OpenAI API key
    filename = 'path_to_your_pdf_file.pdf'
    summary = summarize_pdf(filename)
    print(summary)
```
* Mailing Integration
	* Set up an email service provider (e.g., Gmail, SendGrid) for sending emails programmatically
	* Configure SMTP settings in web application to enable email sending
	* Create email templates for sending abbreviated chapters
	* **Configure daily email sending**
		* Implement a scheduler (e.g., cron job, Celery) to send emails daily
			* Service variants:
			* https://www.beehiiv.com/
		* Develop a script or function to select a new abbreviated chapter each day from the uploaded PDFs
		* Send the selected chapter to subscribers' email addresses
* Intermediate testing
	* Test the web application thoroughly, including file uploads, text summarization, email sending, and scheduled tasks
	* Perform both functional and usability testing to ensure a smooth user experience
* Deploy web application to a hosting platform
	* Choose a hosting provider for deploying your web application (e.g., Heroku, AWS, DigitalOcean)
	* Configure the deployment environment and deploy application
* Monitoring and Maintenance
	* Implement logging and monitoring solutions to track application performance and errors
## Tasks to solve in perspective
* Think about active subscription limitations for every user for not to take up too much space on server
* Think how to effectively adapt web application to different screen sizes and devices
## Users tests
* Organize for few users test of application in different stages of development
## Resources
* https://gemini.google.com/app/b46b00fec05b30d0
* https://chat.openai.com/c/6c35229d-5a47-4c06-bf15-232042f06b8f
* https://chat.openai.com/c/4c2af648-3a3c-4920-9bb7-3b7d3d83728f
* https://gemini.google.com/app/5cf481a53ad28330 
* https://www.phind.com/search?cache=aqo0ydkihxmq9lhvk6mjqxx4