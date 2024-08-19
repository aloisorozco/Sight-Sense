export function runCommands(): boolean {

    let available_resource: "Food" | "Water" | null = null
    let day: number = 1
    let food: number = 5
    let water: number = 5
    let dice_val: number = 0

    while(true){
        if(day == 7){
            return true
        }

        dice_val = rollDice(6,1)

        switch(dice_val){
            case 1:
                available_resource = "Food"
            case 2:
                available_resource = "Water"
            default:
                if(available_resource == null){

                    available_resource = dice_val % 2 == 0 ? "Food": "Water"

                }
                else if(available_resource == "Food"){
                    food += dice_val
                    available_resource = null
                }
                else{
                    water += dice_val
                    available_resource = null
                }
        }


        water--
        food --
        day++

        if(food == 0 || water == 0){
            return false
        }
    }
	
}

function rollDice(max: number, min: number): number{
    return Math.floor(Math.random() * (max - min + 1) + min)
}