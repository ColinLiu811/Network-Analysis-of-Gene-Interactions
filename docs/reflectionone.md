# Sprint Reflection

## 1. What Went Well?

This sprint saw significant progress in building a comprehensive protein-protein interaction network analysis pipeline. Several key accomplishments stand out:

**Successful Pipeline Development**: I successfully created an automated pipeline (`run_pipeline.py`) that orchestrates the entire analysis workflow from data processing through visualization. The pipeline integrates five distinct modules: data download/processing, data cleaning, graph construction, centrality computation, and network visualization. This modular architecture makes the system maintainable and allows each component to be tested independently.

**Robust Data Processing**: The data cleaning module (`clean_data.py`) effectively handles real-world data challenges including missing values, duplicate interactions, self-interactions, and confidence score filtering. Using Pandas for data manipulation proved efficient and readable. The cleaning process successfully reduced 500 example interactions to 449 high-confidence interactions while maintaining data integrity.

**Comprehensive Centrality Analysis**: The centrality computation module (`compute_centrality.py`) successfully implements six different centrality measures: degree, betweenness, closeness, eigenvector centrality, PageRank, and clustering coefficient. The composite hub scoring system effectively combines these metrics to identify biologically significant hub genes. The system correctly identified GENE_0042 as the top hub with 17 connections and a perfect hub score of 1.000.

**Network Visualization**: Static visualizations were successfully generated, including full network views, hub-focused networks, community structures, and summary statistics plots. The visualizations effectively communicate network topology, highlight important nodes, and reveal community structure using the Louvain algorithm, which detected 7 distinct communities in the example network.

**Example Data Generation**: The example data generator (`generate_example_data.py`) provides a valuable testing tool that allows the pipeline to be validated without requiring large STRING database downloads. This facilitated rapid iteration and testing of the entire system.

**Documentation**: Comprehensive documentation including README.md, QUICKSTART.md, and CONTRIBUTING.md provides clear guidance for users and contributors. The documentation explains network metrics, usage patterns, and project structure effectively.

## 2. What Did Not Go Well?

Several challenges emerged during this sprint that require attention:

**Interactive Visualization Failure**: The interactive HTML visualization component encountered a critical error with the pyvis library. The error `AttributeError: 'NoneType' object has no attribute 'render'` indicates that the pyvis template system failed to initialize properly. This suggests either a version compatibility issue with pyvis or a missing dependency. The static visualizations work correctly, but the interactive feature, which would provide significant value for exploring large networks, is currently non-functional.

**Python Interpreter Inconsistency**: The pipeline script (`run_pipeline.py`) uses `python` in subprocess calls, but the system requires `python3`. This caused the automated pipeline to fail, requiring manual execution of individual steps. This is a cross-platform compatibility issue that should be addressed to ensure the pipeline works out-of-the-box on different systems.

**Limited Error Handling**: While individual modules handle errors reasonably well, the pipeline script could benefit from more robust error recovery. When one step fails, the entire pipeline stops without providing clear guidance on how to resume or what intermediate files might be useful for debugging.

**Testing Coverage**: The project lacks comprehensive unit tests for individual modules. While the pipeline runs successfully with example data, there's no systematic testing of edge cases, error conditions, or boundary cases (e.g., very small networks, disconnected graphs, networks with no hub genes).

**Performance Considerations**: The pipeline processes example data quickly, but there's no optimization for large-scale networks. The README mentions that centrality computation can take 2-3 hours for large networks, but there's no progress indication, checkpointing, or parallelization to improve the user experience during long computations.

**Missing Validation**: The pipeline doesn't validate input data formats before processing. If a user provides malformed CSV files or incorrect graph formats, errors may not be caught until deep into the processing pipeline, wasting computation time.

## 3. How Should You Improve?

**Implement Comprehensive Testing Framework**: I should develop a robust testing suite using pytest that covers unit tests for each module, integration tests for the pipeline, and edge case handling. This should include:
- Unit tests for data cleaning functions (handling empty files, malformed data, missing columns)
- Graph construction tests (disconnected components, self-loops, duplicate edges)
- Centrality computation tests (validating mathematical correctness against known network structures)
- Visualization tests (ensuring output files are generated correctly)
- Integration tests that run the full pipeline with various input sizes

This testing framework will catch errors early, provide confidence when refactoring, and serve as documentation for expected behavior.

**Fix Interactive Visualization and Improve Error Handling**: I need to investigate and resolve the pyvis library issue. This may involve:
- Checking pyvis version compatibility and updating if necessary
- Verifying all required dependencies are properly installed
- Adding fallback mechanisms if interactive visualization fails (gracefully degrade to static-only mode)
- Implementing better error messages that guide users toward solutions

Additionally, I should add comprehensive error handling throughout the pipeline:
- Input validation at each stage
- Clear error messages with suggested fixes
- Checkpoint/resume capability for long-running computations
- Progress indicators for computationally intensive steps
- Better handling of missing dependencies with helpful installation instructions

**Enhance Cross-Platform Compatibility**: To address the Python interpreter issue, I should:
- Detect the available Python interpreter (python3, python, py) at runtime
- Use `sys.executable` to ensure subprocess calls use the same interpreter
- Add a configuration option or environment variable for Python path
- Update documentation to specify Python version requirements clearly
- Consider using a shebang line or entry point script for better portability

## 4. What Did You Discover About the Computer Science Topics Identified in the Plan for This Sprint?

**Graph Theory and Network Analysis**: This sprint provided deep practical experience with graph theory concepts. Working with NetworkX revealed the complexity of real-world network structures. The example network demonstrated scale-free properties typical of biological networks, where a few hub nodes have many connections while most nodes have few. Understanding centrality measures in practice highlighted their different interpretations: degree centrality identifies highly connected nodes, betweenness identifies bottlenecks, and eigenvector centrality identifies nodes connected to other important nodes. The Louvain community detection algorithm revealed how networks naturally organize into functional modules, with 7 communities detected in the example network despite its relatively small size.

**Data Processing Pipelines**: Building a multi-stage pipeline taught valuable lessons about data flow, intermediate file formats, and pipeline orchestration. The pipeline demonstrates the importance of modular design—each stage can be tested independently and reused in different contexts. Using CSV for intermediate data and GraphML for graph representation provided flexibility, though I learned that GraphML files can become large for big networks. The experience highlighted the need for data validation at pipeline boundaries and the importance of maintaining data provenance (tracking how data transforms through each stage).

**Algorithm Implementation and Optimization**: Implementing multiple centrality algorithms revealed their computational complexity differences. Degree centrality is O(V) where V is vertices, while betweenness centrality is O(V×E) for unweighted graphs, making it much slower for large networks. This explains why the README mentions 2-3 hour computation times for full human interactome analysis. The composite hub scoring system required careful normalization of different centrality measures, which have different scales and distributions. This taught me about feature scaling and combining heterogeneous metrics.

**Software Engineering Practices**: The project structure evolved to separate concerns (data processing, graph analysis, visualization) into distinct modules. This modularity proved valuable when debugging—I could isolate issues to specific components. However, I also learned that modularity requires careful interface design. The current pipeline uses file-based communication between modules, which is simple but creates tight coupling to file formats. A future improvement might use in-memory data structures or a more formal API between modules.

**Visualization and Data Communication**: Creating effective network visualizations required understanding both the technical aspects (layout algorithms, rendering) and the communication aspects (what information to highlight, how to make complex networks interpretable). The hub-focused visualization successfully emphasizes important nodes, while community visualization reveals network structure. However, I discovered that visualization libraries have limitations—the pyvis error demonstrates how external dependencies can introduce fragility. This highlights the importance of having fallback options and not relying on a single visualization method.
