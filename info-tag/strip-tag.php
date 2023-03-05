#! /usr/bin/env php
<?php
declare(strict_types=1);

require_once 'DOMTraverse.php';
require_once 'Manipulate.php';
require_once 'Share.php';
require_once 'Visit.php';

use app\libraries\info_tag\Manipulate;
use app\libraries\info_tag\Share;

$short_opts = 'c:f:h::';
$long_opts = ['class:', 'file:', 'help::'];

$msg_help =
    "Excise tags of a given class from an HTML DOM node.\n"
    . "-c, --class element class to excise from node\n"
    . "-f --file path to html file. use -- for stdin\n"
    . "-h --help print this help message\n";

$rest_index = -1;
$opts = getopt($short_opts, $long_opts, $rest_index);
if ($opts === false) {
    fwrite(STDERR, "Encountered error when parsing command line arguments\n");
    exit(1);
}
// print_r($opts);

if ($rest_index !== -1 && $rest_index !== $argc) {
    fwrite(
        STDERR,
        sprintf(
            "Error: encountered unrecognized argument: %s\n",
            $argv[$rest_index - 1]
        )
    );
    exit(1);
}

if (array_key_exists('h', $opts) || array_key_exists('help', $opts)) {
    fwrite(STDERR, $msg_help);
    exit(0);
}

if (array_key_exists('c', $opts)) {
    $class = $opts['c'];
} elseif (array_key_exists('class', $opts)) {
    $class = $opts['class'];
} else {
    fwrite(STDERR, "Missing required argument: -c --class\n");
    exit(1);
}

$html = null;

if (array_key_exists('f', $opts)) {
    $path = $opts['f'];
} elseif (array_key_exists('file', $opts)) {
    $path = $opts['file'];
} else {
    $html = stream_get_contents(fopen('php://stdin', 'r'));
    $path = null;
}

if ($path !== null && file_exists($path) && is_readable($path)) {
    $html = stream_get_contents(fopen($path, 'r'));
} elseif ($html === null) {
    fwrite(STDERR, "Could not read file.\n");
    exit(1);
}

$doc = Share::loadHTML($html);
$extracted = Manipulate::excise_tags($doc, $doc, $class);
print($doc->saveHTML());
