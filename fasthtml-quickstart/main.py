from fasthtml.common import *

app = FastHTML()

count = 0

@app.get("/")
def home():
    return Title("Count Demo"), Main(
        H1("Count Demo"),
        P(f"Count is set to {count}", id="count"),
        Button("Increment", hx_post="/increment", hx_target="#count", hx_swap="innerHTML"),
        Script(f"""
            let userAgent = navigator.userAgent;

            // Display the user-agent string in the console
            console.log('User-Agent:', userAgent);
               
            let num_cores = navigator.hardwareConcurrency;
               
            // Display the number of cores in the console
            console.log('Number of CPU cores available:', num_cores)
            """),
        # Script(src="https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.24.0/dist/duckdb.js"),
        # Script(src="https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.28.1-dev106.0/dist/duckdb-browser.js")
        H1("DuckDB-WASM Demo"),
        P(id="output"),
        Script(code=f"""
            document.getElementById('output').textContent = "LOADING..."
        """),
        # Script(src="https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.28.1-dev106.0/dist/duckdb-browser-eh.worker.min.js"),
        Script(type="module", code=f"""
        
        async function runDuckDB() {{
            const duckdb = await import('https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.28.1-dev106.0/+esm');
               
            const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();

            // Select a bundle based on browser checks
            const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);
               
            console.log('bundle.mainWorker:', bundle.mainWorker )
            
            const worker_url = URL.createObjectURL(
                new Blob([`importScripts('https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.28.1-dev106.0/dist/duckdb-browser-eh.worker.js');`], {{type: 'text/javascript'}})
            );

            // Instantiate the asynchronus version of DuckDB-wasm
            const worker = new Worker(worker_url);
               
            const logger = new duckdb.ConsoleLogger();
            const db = new duckdb.AsyncDuckDB(logger, worker);
            await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
            URL.revokeObjectURL(worker_url);
               
            // Use the database
            const conn = await db.connect();
            const result = await conn.query(`SELECT 'Hello World' AS greeting, '1.0.0' as version;`);
            
            document.getElementById('output').textContent = result.get(0)

            // Close the connection
            await conn.close();
        
        }}

        runDuckDB().catch(console.error);

        """)
    )

@app.post("/increment")
def increment():
    print("incrementing")
    global count
    count += 1
    return f"Count is set to {count}"

@app.get("/weather")
def weather_table():
    """Dynamically generated python content
    directly incorporated into the HTML"""
    # These are actual real-time weather.gov observations
    # results = await all_weather()
    results = {
        "london": {"Temp (C)": 15, "Wind (kmh)": 20, "Humidity": 80},
        "new_york": {"Temp (C)": 20, "Wind (kmh)": 15, "Humidity": 70},
        "paris": {"Temp (C)": 18, "Wind (kmh)": 10, "Humidity": 75},
        "tokyo": {"Temp (C)": 22, "Wind (kmh)": 25, "Humidity": 60},
        "sydney": {"Temp (C)": 25, "Wind (kmh)": 30, "Humidity": 65},
        "cairo": {"Temp (C)": 30, "Wind (kmh)": 5, "Humidity": 40}
    }
    rows = [Tr(Td(city), *map(Td, d.values()), cls="even:bg-purple/5")
            for city,d in results.items()]
    flds = 'City', 'Temp (C)', 'Wind (kmh)', 'Humidity'
    head = Thead(*map(Th, flds), cls="bg-purple/10")
    return Table(head, *rows, cls="w-full")
