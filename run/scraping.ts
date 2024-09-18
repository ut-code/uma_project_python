//scrapingで実装したい処理をここに書く

import { ScrapingClient } from "../utils/scraping"

(async () => {
    const scraping = new ScrapingClient()
    await scraping.race({})
})()