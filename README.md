========================= READ ME =========================

This is the Eastek Project Engineering organizational site
created by Ian Harrington (2017).

Developed using Django 1.11 and python 3.5.2

This website is separated into 3 main sections (apps)
    - Employees
    - Overtime
    - Projects

Each section is comprised of models (data representation), views (visual presentation),
forms (allow for data entry), and templates (html structure which is populated by views).
For a better explaination read the offical django site: https://www.djangoproject.com/

In order to change the user interface of the site while keeping the content the same,
it would be sufficient to change just the templates. In order to change the functionality
of the web pages, changes to the views and potentially the forms would be required in
addition to the templates. Changing what data is stored or in what format would require
changes to the model and most likely include changes to all levels of the app. Each of
the apps are dependant on one another. For example, the Overtime app requires the Employee
app to contain a list of the employees so that employee specific overtime data can be
recorded. The project app is the most extensive, and has the most complex models & views.