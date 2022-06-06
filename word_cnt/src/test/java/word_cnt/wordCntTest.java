package word_cnt;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.util.ToolRunner;

public class wordCntTest {
	public static void main(String[] not_used) throws Exception {
		Configuration conf = new Configuration();
		conf.setInt("mapreduce.job.reduces", 3);
		
		String[] args = {"src/test/resources/wikisent2.txt"};
		ToolRunner.run(conf, new WordCount(), args);
	}
}
