<?php

declare(strict_types=1);

namespace app\libraries\info_tag;

class Visit
{
    public const ENTER = 0;
    public const EXIT = 1;
    public const VISIT = 2;

    public int $visit_type;
    public \DOMNode $node;

    public function __construct(int $visit_type, \DOMNode $node)
    {
        $this->visit_type = $visit_type;
        $this->node = $node;
    }
}
