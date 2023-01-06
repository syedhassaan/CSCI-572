<?php

// make sure browsers see this page as utf-8 encoded HTML
header('Content-Type: text/html; charset=utf-8');

$limit = 10;
$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
$results = false;

//$mapping = array();
$file = fopen('/Users/esha/Documents/CSCI 572/hw4/solr-7.7.3/solr-php-client/URLtoHTML_latimes_news.csv', 'r');
while (($line = fgetcsv($file)) !== FALSE) {
  //$line is an array of the csv elements
  $mapping[$line[1]] = $line[0];
  //print_r($line[0]);
}
fclose($file);


//print_r ($mapping);
//echo array_search("e998ba09-d6d1-43c2-bcf8-f4f5ea4cebf7.html",$mapping);




if ($query)
{
  // The Apache Solr Client library should be on the include path
  // which is usually most easily accomplished by placing in the
  // same directory as this script ( . or current directory is a default
  // php include path entry in the php.ini)
  require_once('Apache/Solr/Service.php');

  // create a new solr service instance - host, port, and webapp
  // path (all defaults in this example)
  $solr = new Apache_Solr_Service('localhost', 8983, '/solr/myexample');
  $order = "";

  // if magic quotes is enabled then stripslashes will be needed
  //if (get_magic_quotes_gpc() == 1)
  //{
  //  $query = stripslashes($query);
  //}

  // in production code you'll always want to use a try /catch for any
  // possible exceptions emitted  by searching (i.e. connection
  // problems or a query parsing error)
  try
  {
    $additionalParameters = array(
      'sort' => 'pageRankFile desc'
    );

    if ($_GET['order'] == "PageRank")
    {
      $results = $solr->search($query, 0, $limit, $additionalParameters);
      echo "PageRank";
    } else {
      $results = $solr->search($query, 0, $limit);
      echo "Lucene";
    }
    
  }
  catch (Exception $e)
  {
    // in production you'd probably log or email this error to an admin
    // and then show a special message to the user but for this example
    // we're going to show the full exception
    die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
  }
}

?>
<html>
  <head>
    <title>PHP Solr Client Example</title>
  </head>
  <body>
    <form  accept-charset="utf-8" method="get">
      <label for="q">Search:</label>
      <input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>"/>
      <input type="radio" name="order"  value="Lucene" <?php if (isset($_REQUEST['order']) && $_REQUEST['order'] == 'Lucene')?>>Lucene
      <input type="radio" name="order" value="PageRank"<?php if (isset($_REQUEST['order']) && $_REQUEST['order'] == 'PageRank')?>>PageRank
      <input type="submit"/>
    </form>
<?php

// display results
if ($results)
{
  $total = (int) $results->response->numFound;
  $start = min(1, $total);
  $end = min($limit, $total);
?>
    <div>Results <?php echo $start; ?> - <?php echo $end;?> of <?php echo $total; ?>:</div>
    <ol>
<?php
  // iterate result documents
  foreach ($results->response->docs as $doc)
  {
?>
      <li>
        <table style="border: 1px solid black; text-align: left">
<?php
    // iterate document fields / values
    $url = $doc->og_url;
    if ($url == null or ""){
      $key = substr($doc->id,54);
      $url =  array_search($key,$mapping);
    }
    //echo $url;
    $desc = $doc->description;
    if ($desc == null or ""){
      $desc = "NA";
    }
    if ($desc == null){
      echo "No des";
    } ?>
    <tr>
      <th><?php echo "Title"; ?></th>
      <td><a href = <?php echo $url ?> ><?php echo htmlspecialchars($doc->title, ENT_NOQUOTES, 'utf-8'); ?></a></td>
    </tr>
    <tr>
      <th><?php echo "URL"; ?></th>
      <td><a href = <?php echo $url ?> ><?php echo htmlspecialchars($url, ENT_NOQUOTES, 'utf-8'); ?></a></td>
    </tr>
    <tr>
      <th><?php echo "ID"; ?></th>
      <td><?php echo htmlspecialchars($doc->id, ENT_NOQUOTES, 'utf-8'); ?></td>
    </tr>
    <tr>
      <th><?php echo "Description"; ?></th>
      <td><?php echo htmlspecialchars($desc, ENT_NOQUOTES, 'utf-8'); ?></td>
    </tr>
        </table>
      </li>
<?php
  }
?>
    </ol>
<?php
}
?>
  </body>
</html>
