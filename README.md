# Storytelling Europeana

This project, "Storytelling Europeana", demonstrates how to use the Europeana API to access and tell stories with cultural heritage data from across Europe. It includes a Jupyter notebook that walks through the process of making API calls, working with the returned data, and crafting narratives around the cultural artifacts.

## Project Structure

```bash
.
├── LICENSE
├── README.md
├── environment.yml
└── using_api.ipynb
```

- `LICENSE`: Contains the license information for this project.
- `README.md`: This file, providing project information and setup instructions.
- `environment.yml`: Conda environment specification file.
- `using_api.ipynb`: Jupyter notebook demonstrating the use of the Europeana API for storytelling.

## Setup Instructions

### Prerequisites

- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system.

### Environment Setup

1. Clone this repository to your local machine:

```bash
git clone https://github.com/sg-peytrignet/storytelling-europeana.git
cd storytelling-europeana
```

2. Create the Conda environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
```

3. Activate the newly created environment:

```bash
conda activate glamhack24
```

4. Input your API key in a .env file following the template

### Running the Notebook

1. Start Jupyter Notebook:

```bash
jupyter notebook
```

2. In the Jupyter interface, navigate to and open `using_api.ipynb`.

3. You can now run the cells in the notebook to see how to interact with the Europeana API and create compelling stories with the data.

## Using the Europeana API for Storytelling

The `using_api.ipynb` notebook provides a step-by-step guide on how to:

1. Set up the necessary credentials for the Europeana API.
2. Make API calls to search for cultural heritage items.
3. Process and analyze the returned data.
4. Craft narratives and stories around the cultural artifacts.
5. Visualize results using libraries like matplotlib and geopandas to enhance storytelling.

Make sure to obtain your own API key from the [Europeana Pro website](https://pro.europeana.eu/page/get-api) before running the notebook.

## Contributing

Contributions to improve the notebook, expand the demonstrations, or add new storytelling techniques are welcome. Please feel free to submit a pull request or open an issue if you have any questions or suggestions.

## License

This project is licensed under the terms included in the `LICENSE` file.