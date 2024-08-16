# Concerts I Have Been To (Concerts DB)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)


A simple app to keep track of all the concerts you've been to. Made for my own personal use as a side project.

Right now, I am learning to build a Flask app based on a SQLAlchemy model. This project is a way to practice and learn more about these technologies.

The goal is to have a web interface to visualize all the concerts I have been to and to be able to add new ones.

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


## Dependencies

You can install all the app dependencies using pip with the requirements.txt file.
```python
pip install -r requirements.txt
```

- alembic 1.13.2
- blinker 1.8.2
- click 8.1.7
- Flask 3.0.3
- Flask-Migrate 4.0.7
- Flask-SQLAlchemy 3.1.1
- Flask-WTF 1.2.1
- itsdangerous 2.2.0
- Jinja2 3.1.4
- Mako 1.3.5
- MarkupSafe 2.1.5
- python-dotenv 1.0.1
- SQLAlchemy 2.0.31
- typing_extensions 4.12.2
-  Werkzeug 3.0.3
- WTForms 3.1.2




