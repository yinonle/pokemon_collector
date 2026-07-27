import pytest
from scraper.parser import PokemonParser
from scraper.scraper import PokemonScraper

# Sample HTML fixture representing a mocked PokemonDB page structure
SAMPLE_HTML = """
<html>
  <body>
    <h1>Bulbasaur</h1>
    <table class="vitals-table">
      <tbody>
        <tr>
          <th>National №</th>
          <td><strong>#0001</strong></td>
        </tr>
        <tr>
          <th>Type</th>
          <td>
            <a class="type-icon type-grass" href="/type/grass">Grass</a>
            <a class="type-icon type-poison" href="/type/poison">Poison</a>
          </td>
        </tr>
        <tr>
          <th>Height</th>
          <td>0.7 m (2′04″)</td>
        </tr>
        <tr>
          <th>Weight</th>
          <td>6.9 kg (15.2 lbs)</td>
        </tr>
      </tbody>
    </table>
    <div class="infocard-list-evo">
      <a class="ent-name" href="/pokedex/ivysaur">Ivysaur</a>
    </div>
  </body>
</html>
"""


class TestPokemondbParser:
    """Unit tests for PokemondbParser using mocked HTML content."""

    def test_parse_valid_pokemon_html(self):
        """Tests that HTML is correctly parsed into a structured dictionary."""
        parser = PokemonParser(base_url="https://pokemondb.net")
        result = parser.parse(SAMPLE_HTML)

        assert result["serial_number"] == 1
        assert result["name"] == "Bulbasaur"
        assert result["type"] == "Grass/Poison"
        assert result["height"] == "0.7 m"
        assert result["weight"] == "6.9 kg"
        assert result["evolution_links"] == [
            "https://pokemondb.net/pokedex/ivysaur"
        ]

    def test_parse_missing_vitals_table_raises_value_error(self):
        """Tests that ValueError is raised if vitals table is absent from HTML."""
        parser = PokemonParser(base_url="https://pokemondb.net")
        invalid_html = "<html><body><h1>No Vitals Table Here</h1></body></html>"

        with pytest.raises(ValueError, match="Failed to locate vitals table"):
            parser.parse(invalid_html)


class TestPokemondbScraperIntegration:
    """Integration tests executing real network requests against pokemondb.net."""

    @pytest.fixture
    def scraper(self):
        """Fixture supplying a PokemondbScraper instance."""
        return PokemonScraper()

    def test_scrape_pokemon_by_number(self, scraper):
        """Tests live scraping for Pokemon #1 (Bulbasaur)."""
        data = scraper.scrape_pokemon(1)

        assert data["serial_number"] == 1
        assert data["name"] == "Bulbasaur"
        assert "Grass" in data["type"]
        assert "m" in data["height"]
        assert "kg" in data["weight"]
        assert isinstance(data["evolution_links"], list)

    def test_scrape_pokemon_by_name(self, scraper):
        """Tests live scraping for Pokemon by name ('pikachu')."""
        data = scraper.scrape_pokemon("pikachu")

        assert data["serial_number"] == 25
        assert data["name"] == "Pikachu"
        assert data["type"] == "Electric"

    def test_scrape_non_existent_pokemon_raises_error(self, scraper):
        """Tests that non-existent pokemon triggers 404 ValueError."""
        with pytest.raises(ValueError, match="not found on pokemondb.net"):
            scraper.scrape_pokemon("non_existent_pokemon_xyz_999")
            