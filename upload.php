<?php
    $target_dir = "uploads/";
    $output_dir = "output/";
    $name = str_replace(' ', '', $_POST["name"]);

    $message_file = mt_rand(1000,9999) . $name . '_' . basename($_FILES["messages"]["name"]);
    $timeline_file = mt_rand(1000,9999) . $name . '_' . basename($_FILES["timeline"]["name"]);

    $message_path = $target_dir . $message_file;
    $timeline_path = $target_dir . $timeline_file;

    $i = 1;

    while (file_exists($message_file)) {
        $message_file = $message_file . $i;
        $message_path = $target_dir . $message_file;
        $i++;
    }

    while (file_exists($timeline_file)) {
        $timeline_file = $timeline_file . $i;
        $timeline_path = $target_dir . $timeline_file;
        $i++;
    }

    if(move_uploaded_file($_FILES["messages"]["tmp_name"], $message_path) &&
        move_uploaded_file($_FILES["timeline"]["tmp_name"], $timeline_path)) {

        exec("python $(pwd)/process_fb_files.py " . $message_file . " " . $timeline_file);

        $message_output = explode('.', $message_file);
        $m_output_path = $output_dir . $message_output[0] . ".txt";

        $timeline_output = explode('.', $timeline_file);
        $t_output_path = $output_dir . $timeline_output[0] . ".txt";

        echo "<html>";
        echo "<head><link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"></head>";
        echo "<body>";
        echo "<h2>Results</h2>";
        echo "<h3>Output files</h3>";
        echo "<p>You should be able to click on these links and have your browser open the text files. If not, right click the links below and \"Save as...\" and open the downloaded files.<br>";
        echo "<a target='_blank' href='". $t_output_path ."'>Timeline posts</a><br>";
        echo "<a target='_blank' href='". $m_output_path ."'>Message history</a></p>";
        echo "<h3>Word cloud websites</h3>";
        echo "<p>Copy and paste your results into one (or more, if you want!) of these word cloud generators:<br>";
        echo "<a target='_blank' href=\"https://www.jasondavies.com/wordcloud/\">Word Cloud</a><br>";
        echo "<a target='_blank' href=\"http://www.wordclouds.com/\">Wordclouds</a><br>";
        echo "<a target='_blank' href=\"http://worditout.com/word-cloud/make-a-new-one\">Word It Out</a><br>";
        echo "<a target='_blank' href=\"http://www.wordle.net/create\">Wordle</a><br></p>";
        echo "</body>";
        echo "</html>";

    } else {
        echo "Sorry, it didn't work. You probably need to hit the back button.";
    }
?>