# PHP Pesapal API Integration

This repository contains a PHP project that provides functionality for authenticating with Pesapal APIs and obtaining a Pesapal iframe URL. The project utilizes dependencies stored in the "vendor" folder. Follow the instructions below to run the API and interact with the Pesapal APIs.

## Prerequisites

Before running the project, ensure that you have the following prerequisites installed:

- PHP (>= 8.1)
- Composer (dependency manager for PHP)

## Installation

1. Clone the repository to your local machine by executing the following command in your terminal:
git clone https://github.com/karanidenis/php_project.git

2. Navigate to the project directory:
cd php_project


3. Install project dependencies using Composer:
composer install


## Configuration

1. Open the `pesapal.php` file in the project root directory.

2. Modify the following variables according to your requirements:

- `$secretKey`: Replace `"secretkey"` with your desired secret key for signing and verifying the JWT token.

- Pesapal API credentials:
  - `$payload["consumer_key"]`: Replace `"qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW"` with your Pesapal API consumer key.
  - `$payload["consumer_secret"]`: Replace `"osGQ364R49cXKeOYSpaOnT++rHs="` with your Pesapal API consumer secret.

- Pesapal transaction details:
  - `$payload["url"]`: Replace `"https://www.myapplication.com/ipn"` with the URL where Pesapal IPN (Instant Payment Notification) requests should be sent.
  - `$payload["billing_address"]`: Fill in the relevant details for the billing address.

3. Save the changes.

## Usage

To authenticate with Pesapal APIs and obtain a Pesapal iframe URL, follow these steps:

1. Generate a JWT token by calling the `generateToken()` function. Pass your desired username as a parameter. Example:

<?php
$username = 'admin'; // Replace with your actual username
$token = generateToken($username);
?>```


## Configuration

1. Open the `pesapal.php` file in the project root directory.

2. Modify the following variables according to your requirements:

- `$secretKey`: Replace `"secretkey"` with your desired secret key for signing and verifying the JWT token.

- Pesapal API credentials:
  - `$payload["consumer_key"]`: Replace `"qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW"` with your Pesapal API consumer key.
  - `$payload["consumer_secret"]`: Replace `"osGQ364R49cXKeOYSpaOnT++rHs="` with your Pesapal API consumer secret.

- Pesapal transaction details:
  - `$payload["url"]`: Replace `"https://www.myapplication.com/ipn"` with the URL where Pesapal IPN (Instant Payment Notification) requests should be sent.
  - `$payload["billing_address"]`: Fill in the relevant details for the billing address.

3. Save the changes.

## Usage

To authenticate with Pesapal APIs and obtain a Pesapal iframe URL, follow these steps:

1. Generate a JWT token by calling the `generateToken()` function. Pass your desired username as a parameter. Example:

```php
<?php
$username = 'admin'; // Replace with your actual username
$token = generateToken($username);
?> ```

2.Implement the getIframeUrl() function to obtain the Pesapal iframe URL. This function handles the authentication and registration of IPN. Example:

```<?php
$url = getIframeUrl();
?>
```

3.Use the $token and $url variables as needed in your application.

Example
Here's an example of how to use the provided code:

<?php
require_once __DIR__.'/vendor/autoload.php';

// Your secret key for signing and verifying the JWT
$secretKey = "secretkey";

// Function to generate a JWT token
function generateToken($username)
{
    // Implementation details...
}

// Function to obtain the Pesapal iframe URL
function getIframeUrl()
{
    // Implementation details...
}

// Example usage
$username = 'admin'; // Replace with your actual username
$token = generateToken($username);
$url = getIframeUrl();
echo $token . "\n";
echo $url;
?>

Remember to replace 'admin' with your desired username.

Contributing
If you would like to contribute to this project, please follow the guidelines:

Fork the repository.
Create a new branch for your feature or improvement.
Commit your changes.
Push your changes to your forked repository.
Submit a pull request.