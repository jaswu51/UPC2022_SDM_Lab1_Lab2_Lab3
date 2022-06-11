package struct;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class Vertex implements Serializable {
    private Integer value;
    private List<Long> vertices;

    public Vertex(Integer value) {
        this.value = value;
        this.vertices = new ArrayList<>();
    }

    public Vertex(Integer value, List<Long> vertices) {
        this.value = value;
        this.vertices = vertices;
    }

    public Integer getValue() {
        return value;
    }

    public List<Long> getVertices() {
        return vertices;
    }

    public void setValue(Integer value) {
        this.value = value;
    }

    public void setVertices(List<Long> vertices) {
        this.vertices = vertices;
    }

    public List<Long> addVertex(Long vertex) {
        this.vertices.add(vertex);
        return this.vertices;
    }

    @Override
    public String toString() {
        return "Vertex{" +
                "value=" + value +
                ", vertices=" + vertices +
                '}';
    }
}