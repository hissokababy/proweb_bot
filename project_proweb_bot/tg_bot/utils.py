# функция добавления информации в состояние
def state_add(state, state_argument, info):
    with state.data() as data:
        lst = data.get(state_argument)
        if not lst:
            lst = []
        
    if info not in lst:
        lst.append(info)
        state.add_data(state_argument=lst)
    else:
        lst.remove(info)


    print(lst, 'В ФУНКЦИИ')
    return lst
