# Concerts Database Manager
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

A simple app to keep track of all the concerts you've been to. Made for my own personal use.

This project is a base to learn the SQLAlchemy library.


## Data model


<table>
    <tbody>
        <tr>
            <th>Entity</th>
            <th>Attributes</th>
            <th>Relationships</th>
        </tr>
        <tr>
            <td>Concert</td>
            <td>
                <ul>
                    <li>id</li>
                    <li>date</li>
                    <li>setlist</li>
                    <li>comments</li>
                    <li>ticket</li>
                </ul>
            </td>
            <td>
                <ul>
                    <li>Artist : list of artists playing at the concert (many-to-many relationship)</li>
                    <li>Venue : venue where the concert took place (one-to-one relationship)</li>
                    <li>Photo : list of photos taken at the concert (one-to-many relationship)</li>
                    <li>Video : list of videos taken at the concert (one-to-many relationship)</li>
                    <li>Person : list of people who attended the concert (many-to-many relationship)</li>
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
