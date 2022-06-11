package exercise_4;

import static org.apache.spark.sql.functions.desc;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.io.Writer;

import com.opencsv.CSVParserWriter;
import com.opencsv.CSVWriter;
import com.opencsv.CSVWriterBuilder;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.MetadataBuilder;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.graphframes.GraphFrame;

public class Exercise_4 {

	public static void wikipedia(JavaSparkContext ctx, SQLContext sqlCtx) throws FileNotFoundException {
		File vertices_file = new File(Exercise_4.class.getClassLoader().getResource("wiki-vertices.txt").getFile());
		File edges_file = new File(Exercise_4.class.getClassLoader().getResource("wiki-edges.txt").getFile());

		// Read vertices
		List<Row> vertices_list = new ArrayList<Row>();

		Scanner sc = new Scanner(vertices_file);
		while (sc.hasNext()) {
			String line = sc.nextLine();
			if (line.indexOf('\t') != -1) {
				int index = line.indexOf("\t");
				String id = line.substring(0, index);
				String name = line.substring(index + 1);
				vertices_list.add(RowFactory.create(id, name));
			}
		}
		sc.close();

		// Create Vertices Dataset

		JavaRDD<Row> vertices_rdd = ctx.parallelize(vertices_list);

		StructType vertices_schema = new StructType(new StructField[] {
				new StructField("id", DataTypes.StringType, true, new MetadataBuilder().build()),
				new StructField("name", DataTypes.StringType, true, new MetadataBuilder().build()),
		});

		Dataset<Row> vertices = sqlCtx.createDataFrame(vertices_rdd, vertices_schema);

		List<Row> edges_list = new ArrayList<Row>();

		sc = new Scanner(edges_file);
		while (sc.hasNext()) {
			String line = sc.nextLine();
			if (line.indexOf('\t') != -1) {
				int index = line.indexOf("\t");
				String src_vtx = line.substring(0, index);
				String dest_vtx = line.substring(index + 1);
				edges_list.add(RowFactory.create(src_vtx, dest_vtx));
			}
		}
		sc.close();

		StructType edges_schema = new StructType(new StructField[] {
				new StructField("src", DataTypes.StringType, true, new MetadataBuilder().build()),
				new StructField("dst", DataTypes.StringType, true, new MetadataBuilder().build()),
		});

		JavaRDD<Row> edges_rdd = ctx.parallelize(edges_list);
		Dataset<Row> edges = sqlCtx.createDataFrame(edges_rdd, edges_schema);

		GraphFrame gf = GraphFrame.apply(vertices, edges);
		gf.vertices().show();
		gf.edges().show();

		List<Double> reset_probs = Arrays.asList(0.7);

		List<Integer> max_iters = IntStream.range(20, 21).filter(x -> x % 2 == 0).boxed().collect(Collectors.toList());

		for (Double reset_prob : reset_probs) {
			for (Integer max_iter : max_iters) {
				long start = System.currentTimeMillis();

				GraphFrame pagerank_graph = gf.pageRank().resetProbability(reset_prob).maxIter(max_iter).run();
				pagerank_graph.vertices().orderBy(desc("pagerank")).limit(10).show();

				long end = System.currentTimeMillis();

				System.out.println("\nDamping Factor: " + (1 - reset_prob));
				System.out.println("Reset Prob: " + reset_prob);
				System.out.println("Max Iterations: " + max_iter);
				System.out.println("Time(ms): " + (end - start));

			}
		}

	}
}
