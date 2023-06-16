<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use GuzzleHttp\Client;

// initialize the app
$app = require_once __DIR__.'/../bootstrap/app.php'; // this is the path to your bootstrap/app.php file
$app->make('Illuminate\Contracts\Http\Kernel')->handle(Request::capture()); // this is the line that actually initializes the app  

function get_token() {
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

function register_ipn_token() {
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

function get_iframe_url() {
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
    return redirect($data['redirect_url']);
}

Route::post('/login', function (Request $request) {
    $username = $request->json('username');
    $password = $request->json('password');

    // Example validation - replace with your actual authentication logic
    if ($username == 'admin' && $password == 'password') {
        // Generate JWT token
        $access_token = jwt_encode(['username' => $username]);
        return response()->json(['access_token' => $access_token], 200);
    } else {
        return response()->json(['message' => 'Invalid credentials'], 401);
    }
});

Route::get('/get_iframe_url', function () {
    return get_iframe_url();
})->middleware('jwt');

$app->run();
