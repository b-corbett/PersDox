<?php

declare(strict_types=1);

namespace app\libraries\info_tag;

class Manipulate
{
    public static function excise_tags(\DOMDocument $doc, \DOMNode $root, string $class): void
    {
        foreach (DOMTraverse::dfs_enter_exit_visit($root) as $v) {
            if (($v->visit_type == Visit::EXIT
                            || $v->visit_type == Visit::VISIT)
                    && $v->node->nodeType === XML_ELEMENT_NODE
                    && $v->node->hasAttribute("class")
                    && $v->node->getAttribute("class") === $class) {
                if ($v->node->hasChildNodes()) {
                    $doc_frag = $doc->createDocumentFragment();
                    while ($v->node->childNodes->length != 0) {
                        // appendChild moves the node,
                        // so append until the child count is 0.
                        $doc_frag->appendChild($v->node->childNodes->item(0));
                    }
                    $v->node->parentNode->replaceChild($doc_frag, $v->node);
                } else {
                    $v->node->parentNode->removeChild($v->node);
                }
            }
        }
    }

    public static function extract_elements(\DOMDocument $doc, \DOMNode $root, string $class): array
    {
        $key_id = 'id';
        $key_value = 'value';

        $elements = [];

        foreach (DOMTraverse::dfs_enter_exit_visit($root) as $v) {
            if (($v->visit_type == Visit::EXIT
                            || $v->visit_type == Visit::VISIT)
                    && $v->node->nodeType === XML_ELEMENT_NODE
                    && $v->node->hasAttribute("class")
                    && $v->node->getAttribute("class") === $class) {
                if ($v->node->hasChildNodes()) {
                    $doc_frag = $doc->createDocumentFragment();
                    while ($v->node->childNodes->length != 0) {
                        // appendChild moves the node,
                        // so append until the child count is 0.
                        $doc_frag->appendChild($v->node->childNodes->item(0));
                    }

                    // DOMDocument::saveHTML appends a trailing \n character.
                    // Count number of trailing newlines in the final text node,
                    // and the number of trailing newlines in the output of saveHTML.
                    // Excise any trailing newlines in the output of saveHTML.
                    $num_newlines = 0;
                    if ($doc_frag->lastChild !== null
                            && $doc_frag->lastChild->nodeType === XML_TEXT_NODE
                            && ($len = $doc_frag->lastChild->length) !== 0) {
                        while (--$len !== -1
                                     && $doc_frag->lastChild->data[$len] === "\n") {
                            ++$num_newlines;
                        }
                    }

                    $tmp_doc = new \DOMDocument();
                    $tmp_doc->appendChild($tmp_doc->importNode($doc_frag, true));
                    $value = $tmp_doc->saveHTML($tmp_doc);

                    $num_newlines_out = 0;
                    $len = \mb_strlen($value);
                    while (--$len !== -1 && $value[$len] === "\n") {
                        ++$num_newlines_out;
                    }

                    $num_newlines_diff = $num_newlines_out - $num_newlines;
                    if ($num_newlines_diff > 0) {
                        // print("excess newlines :|\n");
                        // Remove excess newlines.
                        $value = mb_substr($value, 0, mb_strlen($value) - $num_newlines_diff);
                    }

                    $data = [$key_value => $value];

                    // print(sprintf("ntn: %d\n", $num_newlines));
                    // print(sprintf("ntn0: %d\n", $num_newlines_out));
                    // print(sprintf("%s\n", $value));

                    if ($v->node->hasAttribute("id")) {
                        $data[$key_id] = $v->node->getAttribute("id");
                    }
                    $v->node->parentNode->replaceChild($doc_frag, $v->node);
                } else {
                    $data = [$key_value => ''];
                    $v->node->parentNode->removeChild($v->node);
                }
                $elements[] = $data;
            }
        }

        return $elements;
    }
}
