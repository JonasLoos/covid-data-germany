Dieses Repository enthält ausgewählte Covid-Daten des RKI in einem einfachen Format.

Die Daten sind in tägliche Neuinfektionen (cases) und Todesfälle (deaths) pro Landkreis aufgeteilt.

*See below for an English description.*

### Datenformat

Die `.csv` Dateien enthalten je eine Matrix mit `402` Zeilen und `anzahl-der-tage+1` Spalten.
Die erste Zeile enthält ab der zweiten Spalte das Datum (Python `date(...).toordinal()`) vom 1. Jan. 2020 bis zum Dateidatum.
Die erste Spalte enthält ab der zweiten Zeile den [Amtlichen Gemeindeschlüssel (AGS)](https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel) (nur Bundesland und Landkreis).

    0,737060,737061,...
    1001,value-for-first-day-for-1001,value-for-second-day-for-1001,...
    ...
    16077,value-for-first-day-for-16077,value-for-second-day-for-16077,...

### Warum mehrere Dateien

Das RKI veröffentlicht nicht nur Daten für den aktuellen Tag sondern aktualisiert auch vergangene Tage. Deshalb unterscheiden sich die Dateien in mehr als der letzten Spalte.

### Aktuelle Daten

![new data](plots/new_data.png)

### Quellen

Datenquelle: Robert Koch-Institut (RKI), [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0)

Die Daten bis zum 24. Jan. 2020 sind von https://github.com/micb25/RKI_COVID19_DATA. Neue Daten werden einmal täglich heruntergeladen und aktualisiert.


# English Description

This Repo contains parsed Covid-Data from the RKI in a simple format.

The data is split in daily new cases and deaths per county.


### Data Format

The `.csv` files contain a matrix with `402` rows and `number-of-days+1` columns.
The first row contains the ordinal dates (Python `date(...).toordinal()`) from 2020-01-01 until the date of the file, starting at the second column.
The first column contains the German [County Identification Numbers (AGS)](https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel) (federal state and county only), starting at the second row.

    0,737060,737061,...
    1001,value-for-first-day-for-1001,value-for-second-day-for-1001,...
    ...
    16077,value-for-first-day-for-16077,value-for-second-day-for-16077,...

### Why multiple files

The RKI publishes not only data for the current day but also updates the previous days. Therefore the files differ in more than the last column.

### Data Sources

Data Source:  Robert Koch-Institut (RKI), [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0)

Data from until 2020-01-24 is from https://github.com/micb25/RKI_COVID19_DATA. New Data is downloaded and parsed once every day.
