import fs from "fs"
import path from "path"

type horse_data = {
    title: string
    rank: number
    waku: string
    umaban: number
    horse: string
    age: string
    weight: string
    jockey: string
    time: string
    margin: string
    h_weight: number
    h_weight_zougen: number
    f_time: string
    trainer: string
    pop: string
    corner: number[]
}

export async function horse() {
    const files = fs.readdirSync(path.join(__dirname, "../db/jra"))
    let horses = {} as Record<string, horse_data[]>

    for (const file of files) {
        const data = JSON.parse(fs.readFileSync(path.join(__dirname, `../db/jra/${file}`), "utf-8"))
        const title = data["title"]
        for (const horse of data.horse) {
            horse.title = title

            if (horses[horse.horse]) {
                horses[horse.horse].push(horse)
            } else {
                horses[horse.horse] = [ horse ]
            }
        }
    }

    for (const horse of Object.keys(horses)) {
        const data = horses[horse]
        fs.writeFileSync(path.join(__dirname, `../db/horse/${horse}.json`), JSON.stringify(data, null, "\t"))
    }
}
