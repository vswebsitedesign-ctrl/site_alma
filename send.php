<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method not allowed');
}

// Honeypot check
if (!empty($_POST['_honeypot'])) {
    http_response_code(400);
    exit('Bad request');
}

// Sanitise inputs
$name     = htmlspecialchars(strip_tags(trim($_POST['name']     ?? '')));
$phone    = htmlspecialchars(strip_tags(trim($_POST['phone']    ?? '')));
$email    = htmlspecialchars(strip_tags(trim($_POST['email']    ?? '')));
$postcode = htmlspecialchars(strip_tags(trim($_POST['postcode'] ?? '')));
$service  = htmlspecialchars(strip_tags(trim($_POST['service']  ?? '')));
$message  = htmlspecialchars(strip_tags(trim($_POST['message']  ?? '')));

// Basic validation
if (empty($name) || empty($phone) || empty($postcode) || empty($service)) {
    http_response_code(400);
    exit('Missing required fields');
}

// Build email
$to      = 'info@alma-enterprises.co.uk';
$subject = 'New Quote Request - Alma Enterprises';
$body    = "New quote request received from the website.\n\n"
         . "Name:               {$name}\n"
         . "Phone:              {$phone}\n"
         . "Email:              {$email}\n"
         . "Postcode/Location:  {$postcode}\n"
         . "Type of Clearance:  {$service}\n"
         . "Additional Details: {$message}\n";

$headers = "From: noreply@alma-enterprises.co.uk\r\n"
         . "Reply-To: {$email}\r\n"
         . "X-Mailer: PHP/" . phpversion();

$sent = mail($to, $subject, $body, $headers);

if ($sent) {
    header('Location: /thank-you/');
    exit;
} else {
    http_response_code(500);
    exit('Mail error – please call us on 07932 521901');
}
