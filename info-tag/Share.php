<?php

declare(strict_types=1);

namespace app\libraries\info_tag;

// If the document type definition, and html element aren't in the
// HTML fragment passed to loadHTML, then don't add them when
// DOMDocument is serialized back in to HTML.
const load_html_options = \LIBXML_HTML_NODEFDTD | \LIBXML_HTML_NOIMPLIED;

class Share
{
    public static function loadHTML(string $html, int $options = load_html_options): \DOMDocument
    {
        /**
        * Wrapper for DOMDocument::loadHTML with default options and xmllib error reporting turned on.
         * Use libxml internal errors: libxml_use_internal_errors(true).
         * Default options for DOMDocument::loadHTML are \LIBXML_HTML_NODEFDTD | \LIBXML_HTML_NOIMPLIED.
        */
        // https://www.php.net/manual/en/domdocument.loadhtml.php
        // From the Description section:
        // "This function may also be called statically to load and create a DOMDocument object."
        // From the Errors/Exceptions section:
        // Prior to PHP 8.0.0 this method could be called statically, but would issue an E_DEPRECATED error.
        // As of PHP 8.0.0 calling this method statically throws an Error exception
        // PHP documentation, you so cray <3.

        \libxml_use_internal_errors(true);
        $doc = new \DOMDocument();
        $doc->loadHTML($html, $options);

        return $doc;
    }
}
