# Concerts I Have Been To (Concerts DB)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)


A simple app to keep track of all the concerts you've been to. Made for my own personal use as a side project.

Right now, I am learning to build a Flask app based on a SQLAlchemy model. This project is a way to practice and learn more about these technologies.

The goal is to have a web interface to visualize all the concerts I have been to and to be able to add new ones.

## How to install and run the app

Clone this git repository.
```bash
git clone https://github.com/MathieuGood/concerts_db.git
```

Navigate to the project folder, create a virtual environment and activate it.
```bash
cd concerts_db
python -m venv venv
source venv/bin/activate
```

Install all the dependencies.
```python
pip install -r requirements.txt
```

Run the app.
```bash
python run.py
```


## Data model

Show is the main entity of the model :
- It represents an event held at a certain date and place (Venue).
- A show can have multiple Concerts, each one performed by an Artist.
- It can be part of a Festival.
- It can have multiple Persons attending it.


<table>
    <tbody>
        <tr>
            <th>Entity</th>
            <th>Attributes</th>
            <th>Relationships</th>
        </tr>
         <tr>
            <td>Show</td>
            <td>
                <ul>
                    <li>id : autoincrementing integer</li>
                    <li>name : varchar</li>
                    <li>event_date : date</li>
                    <li>comments : varchar</li>
                    <li>ticket_path : varchar</li>
                </ul>
            </td>
            <td>
                <ul>
                    <li>Concert : list of concerts performed at the show (one-to-many relationship)</li>
                    <li>Venue : venue where the show took place (many-to-one relationship)</li>
                    <li>Festival : festival where the show took place (many-to-one relationship)</li>
                    <li>Person : list of people who attended the show (many-to-many relationship)</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Concert</td>
            <td>
                <ul>
                    <li>id : autoincrementing integer</li>
                    <li>setlist : varchar</li>
                    <li>comments : varchar</li>
                </ul>
            </td>
            <td>
                <ul>
                    <li>Artist : artist performing the concert (one-to-many relationship)</li>
                    <li>Photo : list of photos taken at the concert (one-to-many relationship)</li>
                    <li>Video : list of videos taken at the concert (one-to-many relationship)</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Artist</td>
            <td>
                <ul>
                    <li>id : unique autoincrementing integer</li>
                    <li>country : varchar</li>
                </ul>
            </td>
            <td>
            </td>
        </tr>
        <tr>
            <td>Venue</td>
            <td>
                <ul>
                    <li>id : unique autoincrementing integer</li>
                    <li>name : varchar</li>
                </ul>
            </td>
            <td>
                <ul>
                    <li>Address : address of the venue (many-to-one relationship)</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>Address</td>
            <td>
                <ul>
                    <li>id : unique autoincrementing integer</li>
                    <li>city : varchar</li>
                    <li>country : varchar</li>
                </ul>
            </td>
            <td></td>
        </tr>
        <tr>
            <td>Photo</td>
            <td>
                <ul>
                    <li>id : unique autoincrementing integer</li>
                    <li>path : varchar</li>
                </ul>
            </td>
            <td></td>
        </tr>
        <tr>
            <td>Video</td>
            <td>
                <ul>
                    <li>id : unique autoincrementing integer</li>
                    <li>path : varchar</li>
                </ul>
            </td>
            <td></td>
        </tr>
        <tr>
            <td>Person</td>
            <td>
                <ul>
                    <li>id : unique autoincrementing integer</li>
                    <li>firstname : varchar</li>
                    <li>lastname : varchar</li>
                </ul>
            </td>
            <td></td>
    </tbody>
</table>

