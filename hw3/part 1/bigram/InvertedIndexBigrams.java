import java.io.IOException;
import java.util.StringTokenizer;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class InvertedIndexBigrams {

	public static class TokenizeMapper
		extents Mapper<Object, Text, Text, Text>{

		private Text key = new Text();
		private Text value = new Text();

		public void map(Object key, Text value, Context context
                ) throws IOException, InterruptedException {

			String[] key_value = value.toString().split("\t", 2);
			key.set(key_value[0]);

			String val = key_value[1].toLowerCase().replaceAll("[^a-z]+", " ");

	      	StringTokenizer itr = new StringTokenizer(val);
	      	String prev = itr.nextToken();
	        while (itr.hasMoreTokens()) {
	          curr = itr.nextToken();
	          value.set(prev + " " + curr);
	          context.write(value, key);
	          prev = curr;
	        }
	    }
	}

	public static class IntSumReducer
       extends Reducer<Text,Text,Text,Text> {

	    //private IntWritable result = new IntWritable();

	    public void reduce(Text key, Iterable<Text> IDs,
	                       Context context
	                       ) throws IOException, InterruptedException {

	    	Map<String, Integer> word_count = new HashMap<>();

	    	for (Text id:IDs) {
	    		String id_ = id.toString();
	    		word_count.put(id_, word_count.get0orDefault(id_, 0) + 1);
	    	}

	    	StringBuilder output = new StringBuilder();

	    	for (Map.Entry<String, Integer> key_ val : word_count.entrySet()) {
	    		output.append(key_val.getKey()).append(":").append(key_val.getValue());
	    	}

	    	private Text result = new Text(word_count.toString());

	    	context.write(key, result);
    	}
  	}

  	public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "word count");
    job.setJarByClass(WordCount.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }

}