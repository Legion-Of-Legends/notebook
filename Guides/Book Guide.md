# Book Guide
This page is about the [Book](../Books) guide. How you can add new book and use it to keep track of your reading progress and keep notes of it.
## Steps to add a new book
1. Open the Book Note page. [link](../Books/Books%20Notes)
2. Create a new markdown file with the name of the book you want to add, following this format: `Test Book.md`.
3. Add the following template to the newly created markdown file:
   ```markdown
   # Book Title

   ## Chapter 1: Title of Chapter 1
   chapter 1 content goes here.
   ## Chapter 2: Title of Chapter 2
   chapter 2 content goes here.
   ```
> [!NOTE]
> This format may vary depending on the book, but it is recommended to keep the chapter structure for better organization. IT'S FULLY OPTIONAL.
4. Save the file in the `Books Notes` folder.
5. Open the Books page. [link](../Books)
6. Edit the `README.md` file in the `Books` folder.
7. Add a new book entry in the following format at the end of the markdown table you see there:
   ```markdown
   |[<Test Book>](./Books%20Notes/<Test%20Book.md>)| <Author>| <Gener>|[<Your name>](https://github.com/<Your Github Username>)|<Current Reading Page>|![Status](https://img.shields.io/badge/<Status>-<Color>?style=plastic)|<Start date>|<End date>|
     ↑↑↑↑↑↑↑↑↑↑↑↑↑                   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑     ↑↑↑↑↑↑↑     ↑↑↑↑↑    ↑↑↑↑↑↑↑↑↑↑↑                       ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑                                          ↑↑↑↑↑↑↑   ↑↑↑↑↑↑                  ↑↑↑↑↑↑↑↑↑↑↑↑   ↑↑↑↑↑↑↑↑↑
   ```
> [!NOTE]
> Replace only the placeholders(`<`PlACEHOLDER`>`) with the actual values for the book you are adding. For you help the editable fields are also marked with these `↑` below them.
> Here is a placeholder description of each field:
> - `<Test Book>`: The title of the book.
> - `<Test%20Book.md>`: The name of the markdown file you created in step 2. Note that spaces are replaced with `%20`.
> - `<Author>`: The author of the book.
> - `<Gener>`: The genre of the book.
> - `<Your name>`: Your name or username.
> - `<Your Github Username>`: Your GitHub username.
> - `<Current Reading Page>`: The current page you are on in the book.
> - `<Status>`: The status of the book. There is three options: `Reading`, `Completed`, `Paused` ,and `Not Started`.
> - `<Color>`: The color of the status badge. It can be `green`, `blue`, or `red` depending on the status. Reading=`green`, Completed=`blue`, Paused=`red`, Not Started=`red`.
> - `<Start date>`: The date you started reading the book.
> - `<End date>`: The date you finished reading the book. If you haven't finished it yet, you can write `-`.
8. Preview the changes to make sure everything looks good.
9. Commit the changes with a meaningful message, such as "Added new book: Test Book".
10. Push the changes to the repository.


That's it! You have successfully added a new book to the Books guide. You can now keep track of your reading progress and take notes on the book.


