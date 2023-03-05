<?php

declare(strict_types=1);

namespace app\libraries\info_tag;

class DOMTraverse
{
    public static function dfs_enter_exit_visit(\DOMNode $node)
    {
        /**
         * Enter internal nodes, and visit leaf nodes in depth first order.
         * Exit internal nodes by backtracking along depth first search path.
         * Yields a Visit instance containing the visit type ()
         **/

        $stack = [$node];
        $partial_dfs = [];

        while ($stack) {
            $stack_ind = count($stack) - 1;
            $node = $stack[$stack_ind];

            $partial_dfs_ind = count($partial_dfs) - 1;

            $is_final =
                    $partial_dfs_ind !== -1
                    && $partial_dfs[$partial_dfs_ind] === $node;

            if ($node->hasChildNodes()) {
                if ($is_final) {
                    // Exiting node.
                    array_pop($stack);
                    array_pop($partial_dfs);
                    yield new Visit(Visit::EXIT, $node);

                    continue;
                }

                // Entering node.
                $partial_dfs[] = $node;
                for ($n = $node->childNodes->length - 1; $n !== -1; --$n) {
                    $stack[] = $node->childNodes->item($n);
                }
                yield new Visit(Visit::ENTER, $node);

                continue;
            }

            // Visiting leaf node.
            array_pop($stack);
            yield new Visit(Visit::VISIT, $node);
        }
    }
}
