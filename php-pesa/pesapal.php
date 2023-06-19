<?php

use GuzzleHttp\Client;
use Firebase\JWT\JWT;

require_once __DIR__.'/vendor/autoload.php'; // Load Composer autoload.php

// Your secret key for signing and verifying the JWT
$secretKey = "secretkey";

// Function to generate a JWT token
function generateToken($username)
{
    global $secretKey;
    $tokenPayload = [
        'username' => $username,
        'iat' => time(),
        'exp' => time() + (60 * 60) // Token expiration time (1 hour from the current time)
    ];
    $token = JWT::encode($tokenPayload, $secretKey, 'HS256');
    return $token;
}

// Function to verify and decode the JWT token
function verifyToken($token)
{
    global $secretKey;
    try {
        $decodedToken = JWT::decode($token, $secretKey, ['HS256']);
        return $decodedToken;
    } catch (\Exception $e) {
        // Token is invalid or expired
        return null;
    }
}

function get_token()
{
    $url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken";
    $headers = ["Content-Type" => "application/json"];

    $payload = [
        "consumer_key" => "qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW",
        "consumer_secret" => "osGQ364R49cXKeOYSpaOnT++rHs="
    ];

    $client = new Client();
    $response = $client->post($url, [
        "headers" => $headers,
        "json" => $payload
    ]);

    $data = json_decode($response->getBody(), true);
    return $data["token"];
}

function register_ipn_token()
{
    $token = "Bearer " . get_token();
    $url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN";

    $headers = [
        "Authorization" => $token,
        "Content-Type" => "application/json",
    ];

    $payload = [
        "url" => "https://www.myapplication.com/ipn",
        "ipn_notification_type" => "GET"
    ];

    $client = new Client();
    $response = $client->post($url, [
        "headers" => $headers,
        "json" => $payload
    ]);

    $data = json_decode($response->getBody(), true);
    return $data["ipn_id"];
}

function get_iframe_url()
{
    $token = "Bearer " . get_token();
    $generated_id = register_ipn_token();
    $url = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest";

    $headers = [
        "Authorization" => $token,
        "Content-Type" => "application/json",
    ];

    $payload = [
        "id" => $generated_id,
        "currency" => "KES",
        "amount" => 100.00,
        "description" => "Payment description goes here",
        "callback_url" => "https://www.myapplication.com/response-page",
        "notification_id" => "fe078e53-78da-4a83-aa89-e7ded5c456e6",
        "billing_address" => [
            "email_address" => "",
            "phone_number" => "",
            "country_code" => "",
            "first_name" => "",
            "middle_name" => "",
            "last_name" => "",
            "line_1" => "",
            "line_2" => "",
            "city" => "",
            "state" => "",
            "postal_code" => "01000",
            "zip_code" => "01000"
        ]
    ];

    $client = new Client();
    $response = $client->post($url, [
        "headers" => $headers,
        "json" => $payload
    ]);

    $data = json_decode($response->getBody(), true);
    return $data['redirect_url'];
}

// Example usage
$username = 'admin'; // Replace with your actual username
$token = generateToken($username);
$url = get_iframe_url();
echo $token . "\n";
echo $url;

