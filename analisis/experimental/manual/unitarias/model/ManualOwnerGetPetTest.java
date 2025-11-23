package org.springframework.samples.petclinic.owner;

public class ManualOwnerGetPetTest {

	public static void main(String[] args) {

		System.out.println("=========== TEST getPet() ===========");

		Owner owner = new Owner();

		// Pet guardado (id != null)
		Pet saved = new Pet();
		saved.setId(10);
		saved.setName("Lucky");
		owner.addPet(saved);

		// Pet nuevo (id == null)
		Pet unsaved = new Pet();
		unsaved.setName("Bobby");
		owner.addPet(unsaved);

		// Pet duplicado en nombre
		Pet duplicate = new Pet();
		duplicate.setName("Lucky");
		owner.addPet(duplicate);

		// ----------- Pruebas por nombre -----------

		System.out.println("\nCaso 1 - Buscar por nombre existente (Lucky):");
		System.out.println("Resultado: " + owner.getPet("Lucky"));

		System.out.println("\nCaso 2 - Buscar por nombre inexistente (Rocky):");
		System.out.println("Resultado: " + owner.getPet("Rocky"));

		System.out.println("\nCaso 3 - Búsqueda case-insensitive (lUcKy):");
		System.out.println("Resultado: " + owner.getPet("lUcKy"));

		System.out.println("\nCaso 4 - Nombre duplicado (Lucky), debe retornar el primero:");
		Pet found = owner.getPet("Lucky");
		System.out.println("¿Corresponde al primero guardado? " + (found == saved));

		// ----------- Pruebas con ignoreNew -----------

		System.out.println("\nCaso 5 - Pet nuevo con ignoreNew=true (Bobby): ");
		System.out.println("Resultado: " + owner.getPet("Bobby", true));

		System.out.println("\nCaso 6 - Pet nuevo con ignoreNew=false (Bobby): ");
		System.out.println("Resultado: " + owner.getPet("Bobby", false));

		// ----------- Pruebas por ID -----------

		System.out.println("\nCaso 7 - Búsqueda por id existente (10):");
		System.out.println("Resultado: " + owner.getPet(10));

		System.out.println("\nCaso 8 - ID pertenece a pet nuevo (null id ignorado):");
		System.out.println("Resultado: " + owner.getPet((Integer) null));

		System.out.println("\nCaso 9 - ID inexistente (99):");
		System.out.println("Resultado: " + owner.getPet(99));

		// ----------- Casos adicionales -----------

		System.out.println("\nCaso 10 - Pet con nombre null no causa error:");
		Pet nullNamePet = new Pet();
		nullNamePet.setId(25);
		nullNamePet.setName(null);
		owner.addPet(nullNamePet);
		System.out.println("Resultado búsqueda null: " + owner.getPet((String) null));

		System.out.println("\nCaso 11 - Lista vacía (nuevo Owner):");
		Owner emptyOwner = new Owner();
		System.out.println("Resultado en vacío: " + emptyOwner.getPet("Lucky"));
	}

}
