

function Inputbox(props){


    return (
        <div classStyle = 'container'>
            <label for="{ props.type }">{ props.type }</label>
            <input type="{ props.type }" id="{ props.type }" placeholder="{ props.text }" required></input>
        </div>
    );
}


export default Inputbox;