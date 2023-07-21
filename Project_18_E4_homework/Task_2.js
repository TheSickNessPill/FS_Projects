// Написать функцию, которая принимает в качестве аргументов строку и объект,
// а затем проверяет есть ли у переданного объекта свойство с данным именем.
// Функция должна возвращать true или false.


function is_prop_in_obj(key, obj){
	if (obj.hasOwnProperty(key)){
		return true
	return false
}
