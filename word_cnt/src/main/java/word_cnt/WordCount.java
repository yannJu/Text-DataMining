package word_cnt;

import java.io.IOException;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class WordCount extends Configured implements Tool {

	public int run(String[] args) throws Exception, IOException {
		// TODO Auto-generated method stub
		Job myjob = Job.getInstance(getConf());
		myjob.setJarByClass(WordCount.class);
		
		myjob.setMapperClass(wordCntMapper.class);
		myjob.setReducerClass(wordCntReducer.class);
		
		myjob.setMapOutputKeyClass(Text.class);
		myjob.setMapOutputValueClass(IntWritable.class);
		
		myjob.setOutputFormatClass(TextOutputFormat.class);
		myjob.setInputFormatClass(TextInputFormat.class);
		
		FileInputFormat.addInputPath(myjob, new Path(args[0]));
		FileOutputFormat.setOutputPath(myjob, new Path(args[0]).suffix(".out"));
		
		myjob.waitForCompletion(false);
		return 0;
	}
	
	
	public static void main(String[] args) throws Exception{
		ToolRunner.run(new WordCount(), args);
	}
	
}
