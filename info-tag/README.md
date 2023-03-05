# A simple PHP library for manipulating an HTML DOMDocument

## Functionality
* Strip tags of a given class from an HTML document fragment
* Extract a document fragments between tags of a given class from an HTML document fragment 

This library has two related purposes.
The first is to extract substrings from the HTML output of solvers, so they can be tested against expected strings.
The second is to strip the tags from the HTML solutions, so they don't interfere with the rendering of LaTeX they may contain.

Ths substrings are delimited by HTML tags of a given class, where any class can be specified.
The default class is "he-info".


## Command line usage
The PHP scripts `strip-tag.php` and `extract-tag.php` provide the core functionality of the library on the command line.
Use the `--help` argument for usage details. 

`strip-tag.php` strips tags of a given class from an HTML string, and outputs the result in HTML format.
`extract-tag.php` extracts the content between all tags of a given class, and outputs the result in JSON format.

Given `test.html`:
```json
<div class="he-info"><p>\[\text{slope} = <span class="he-info" id="he-info-solver-answer">\frac{2}{5}</span>\]</p><br/><p>The slope of the line through the two distinct points \((x_1, y_1)\) and \((x_2, y_2)\), where \(x_1 \ne x_2\), is given by the formula: \[\text{slope} = \frac{y_2 - y_1}{x_2 - x_1}\]</p><p>\[\begin{aligned}\text{slope} &amp;= \frac{y_2-y_1}{x_2-x_1} \\ &amp;= \frac{-2 - -4}{2 - -3} \\ &amp;= \frac{2}{5} \\ &amp;= \frac{2}{5}\end{aligned}\]</p></div>
```

The output of `./strip-tag.php -c 'he-info' -f test.html` is:
```html
<p>\[\text{slope} = \frac{2}{5}\]</p><br><p>The slope of the line through the two distinct points \((x_1, y_1)\) and \((x_2, y_2)\), where \(x_1 \ne x_2\), is given by the formula: \[\text{slope} = \frac{y_2 - y_1}{x_2 - x_1}\]</p><p>\[\begin{aligned}\text{slope} &amp;= \frac{y_2-y_1}{x_2-x_1} \\ &amp;= \frac{-2 - -4}{2 - -3} \\ &amp;= \frac{2}{5} \\ &amp;= \frac{2}{5}\end{aligned}\]</p>
```

The output of `./extract-tag.php -c 'he-info' -f /tmp/tmp.html` is:
```json
[{"value":"\\frac{2}{5}","id":"he-info-solver-answer"},{"value":"<p>\\[\\text{slope} = \\frac{2}{5}\\]<\/p><br><p>The slope of the line through the two distinct points \\((x_1, y_1)\\) and \\((x_2, y_2)\\), where \\(x_1 \\ne x_2\\), is given by the formula: \\[\\text{slope} = \\frac{y_2 - y_1}{x_2 - x_1}\\]<\/p><p>\\[\\begin{aligned}\\text{slope} &amp;= \\frac{y_2-y_1}{x_2-x_1} \\\\ &amp;= \\frac{-2 - -4}{2 - -3} \\\\ &amp;= \\frac{2}{5} \\\\ &amp;= \\frac{2}{5}\\end{aligned}\\]<\/p>"}]
```

Among other important information in the answer, the $`LaTeX`$ representation of the answer is `\frac{2}{5}`, which is delimited with the `span` tag with class "he-info" and id "he-info-solver-answer".
