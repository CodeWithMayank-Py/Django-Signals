# Django Signals Example

This repository demonstrates how to use **Django Signals** to perform actions such as sending an email when a user registers and triggering notifications or actions before deleting a record. The example covers the following:

- **Concepts of Django Signals**
- **Practical Implementation** using Django's `post_save` and `pre_delete` signals.

## Table of Contents

1. [Introduction to Django Signals](#introduction-to-django-signals)
2. [Django Built-in Signals](#django-built-in-signals)
3. [Connecting and Disconnecting Signals](#connecting-and-disconnecting-signals)
4. [Common Use Cases](#common-use-cases)
5. [Implementation Guide](#implementation-guide)
   - [Send Email on New User Registration (`post_save`)](#send-email-on-new-user-registration-post_save)
   - [Trigger Action Before Deleting a Post (`pre_delete`)](#trigger-action-before-deleting-a-post-pre_delete)
6. [Setup and Installation](#setup-and-installation)
7. [Running the Project](#running-the-project)

---

## Introduction to Django Signals

**Signals** are Django’s way to allow decoupled applications to get notified when certain events occur. For example, you might want to trigger an email whenever a new user registers or log an action when a record is deleted.

### How Do Signals Work?

- **Sender**: The model or class that sends a signal.
- **Receiver**: The function or method that listens for a signal and responds to it.
- **Signal**: The event or notification being sent, which can trigger various actions.

In Django, signals provide a way to connect pieces of code that need to run when certain events happen, such as saving an object or deleting a record.

---

## Django Built-in Signals

Django provides several built-in signals, the most common ones include:

- **`pre_save`**: Triggered before a model’s `save()` method is called.
- **`post_save`**: Triggered after a model’s `save()` method is called.
- **`pre_delete`**: Triggered before a model’s `delete()` method is called.
- **`post_delete`**: Triggered after a model’s `delete()` method is called.
- **`m2m_changed`**: Triggered when a many-to-many relationship is changed.
  
For a full list of built-in signals, refer to the [official Django documentation](https://docs.djangoproject.com/en/stable/ref/signals/).

---

## Connecting and Disconnecting Signals

To use signals in Django, you typically use the `@receiver` decorator to connect a receiver function to a signal:

### Connecting a Signal

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import MyModel

@receiver(post_save, sender=MyModel)
def my_signal_receiver(sender, instance, created, **kwargs):
    # Your logic here
    pass
```

### Disconnecting a Signal

If needed, you can disconnect signals using the `disconnect()` method. This can be useful if you want to temporarily stop listening to a signal.

```python
from django.db.models.signals import post_save
from myapp.signals import my_signal_receiver
from myapp.models import MyModel

# Disconnecting the signal
post_save.disconnect(my_signal_receiver, sender=MyModel)
```

### Common Use Cases
Django signals can be used in many scenarios, such as:
- **Logging user actions:** Automatically log changes to important models.
- **Sending notifications:** Send emails or other notifications upon specific events, like user registration.
- **Data validation:** Trigger custom validation or clean-up actions on save or delete events.

### Implementation Guide
#### Send Email on New User Registration (```post_save```)

In this example, we will use the post_save signal to send a welcome email when a new user registers.

**Steps**
1. **Signal Setup:** The signal listens to the ```post_save``` event on the ```User``` model.
2. **Condition:** If a new user is created (i.e., ```created=True```), an email is sent to the new user.

**Code:**
```python
# accounts/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Welcome to Our Site!',
            message=f'Thank you for registering, {instance.username}!',
            from_email='from@example.com',
            recipient_list=[instance.email],
            fail_silently=False,
        )

```

The email will be sent each time a new user is created. Ensure you configure your email backend in ```settings.py```:
```python
# signal_example/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### Trigger Action Before Deleting a Post (```pre_delete```)

We will use the ```pre_delete``` signal to trigger an action before deleting a ```Post``` record. For instance, logging or notifying admins before a post is deleted.

**Steps:**
1. **Signal Setup:** The signal listens to the ```pre_delete``` event on the ```Post``` model.
2. **Action:** Before the ```Post``` is deleted, the signal logs the post title to the console.
Code:

```python
# accounts/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Post

@receiver(pre_delete, sender=Post)
def notify_before_post_delete(sender, instance, **kwargs):
    print(f"Post titled '{instance.title}' is about to be deleted.")

```
When a ```Post``` is deleted, the signal prints a message to the console, logging the title of the post being deleted.

## Setup and Installation

### Step 1: Clone the Repository

```python
git clone https://github.com/CodeWithMayank-Py/Django-Signals
cd signalEX
```

### Step 2: Install Dependencies
Make sure you have Django installed:
```python
pip install django
```

### Step 3: Run Migrations
Run the migrations to create the necessary database tables:
```python
python manage.py migrate
```

### Step 4: Configure Email Backend (Optional)
To test the email functionality, configure the email backend in ```settings.py```. For testing purposes, you can use the console email backend, which will output emails to the terminal:
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
For production use, configure an actual email service like SMTP, Gmail, etc.

## Running the Project

### Step 1: Create a Superuser

To test the user registration email signal, create a superuser by running the following command:

```python
python manage.py createsuperuser
```

Follow the prompts to create the superuser account.

### Step 2: Run the Development Server
Start the Django development server with:
```python
python manage.py runserver
```

### Step 3: Test the User Registration Signal
1. Open your browser and go to the Django admin site: ```http://127.0.0.1:8000/admin/```.

2. Log in using the superuser account you just created.

3. In the admin panel, go to Users and click on Add user to register a new user.

4. Once the user is registered, the ```post_save``` signal will trigger and send a welcome email to the new user's email address.

| Note: If you have configured the email backend as ```console```, you can check the email in your terminal.

### Step 4: Test the Post Deletion Signal
1. First, create a ```Post``` in the Django admin panel. You may need to add it to the admin if it's not visible.
2. Then, delete the post.
3. The ```pre_delete``` signal will trigger, and you should see a message in the terminal logging the post title before it's deleted.


### Conclusion
This repository demonstrates how to implement Django signals to handle various automated tasks, such as sending welcome emails to new users and triggering actions before a post is deleted. Signals provide a clean and decoupled way to handle events in Django, allowing for flexibility and maintainability.

Feel free to expand on this implementation with more advanced signals or other use cases!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Mayank Paliwal** - [CodeWithMayank-Py](https://github.com/CodeWithMayank-Py)























