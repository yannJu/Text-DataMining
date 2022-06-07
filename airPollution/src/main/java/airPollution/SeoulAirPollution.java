package airPollution;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class SeoulAirPollution extends Configured implements Tool {
	public int run(String[] args) throws Exception, IOException {
		// TODO Auto-generated method stub
		String inputPath = args[0];
		
		runP1(inputPath);
		runP2(inputPath);
		runP3(inputPath);
		runP4(inputPath);
		return 0;
	}
	
	public void runP1(String inputPath) throws Exception {
		String outputPath = inputPath + "_p1.out";
		Job job = Job.getInstance(getConf());
		job.setJarByClass(SeoulAirPollution.class);
		
		job.setMapperClass(p1_getAveMaxMinMapper.class);
		job.setReducerClass(p1_getAveMaxMinReducer.class);
		
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(FloatWritable.class);
		
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		
		FileInputFormat.addInputPath(job,  new Path(inputPath));
		FileOutputFormat.setOutputPath(job, new Path(outputPath));
		
		job.waitForCompletion(true);
	}
	
	public void runP2(String inputPath) throws Exception {
		String outputPath = inputPath + "_p2.out";
		Job job = Job.getInstance(getConf());
		job.setJarByClass(SeoulAirPollution.class);
		
		job.setMapperClass(p2_getAirGoodStateMapper.class);
		job.setReducerClass(p2_getAirGoodStateReducer.class);
		
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(IntWritable.class);
		
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		
		FileInputFormat.addInputPath(job,  new Path(inputPath));
		FileOutputFormat.setOutputPath(job, new Path(outputPath));
		
		job.waitForCompletion(true);
		
		String stationCode = "", maxStation = "";
		int averVal, maxVal = Integer.MIN_VALUE;
		
		// 좋음이 제일 많은 지역 찾기 reduce 3개 기준
		for (int i = 0; i < 3; i++) {
			String str, pathTmp = outputPath + "/part-r-0000" + i;
			BufferedReader reader = new BufferedReader(new FileReader(pathTmp));
			while ((str = reader.readLine()) != null) {
				StringTokenizer st = new StringTokenizer(str.toString());
				stationCode = st.nextToken();
				averVal = Integer.parseInt(st.nextToken());
				if (maxVal < averVal) {
					maxVal = averVal;
					maxStation = stationCode;
				}
			}
		}
		
		System.out.println("(MAX) Station Code : " + maxStation + " Val : " + maxVal);
	}
	
	public void runP3(String inputPath) throws Exception {
		String outputPath = inputPath + "_p3.out";
		Job job = Job.getInstance(getConf());
		job.setJarByClass(SeoulAirPollution.class);
		
		job.setMapperClass(p3_recordTransMapper.class);
		job.setReducerClass(p3_recordTransReducer.class);
		
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		
		FileInputFormat.addInputPath(job,  new Path(inputPath));
		FileOutputFormat.setOutputPath(job, new Path(outputPath));
		
		job.waitForCompletion(true);
	}
	
	public void runP4(String inputPath) throws Exception {
		String outputPath = inputPath + "_p4.out";
		Job job = Job.getInstance(getConf());
		job.setJarByClass(SeoulAirPollution.class);
		
		job.setMapperClass(p4_averAirPolwithTimeMapper.class);
		job.setReducerClass(p4_averAirPolwithTimeReducer.class);
		
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		
		FileInputFormat.addInputPath(job,  new Path(inputPath));
		FileOutputFormat.setOutputPath(job, new Path(outputPath));
		
		job.waitForCompletion(true);
	}
	
	public static void main(String[] args) throws Exception {
		ToolRunner.run(new SeoulAirPollution(), args);
	}
}