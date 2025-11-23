package org.springframework.samples.petclinic.owner;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.*;

class OwnerGetPetUnitManualTest {

	private Owner owner;

	private Pet pet1;

	private Pet pet2;

	private Pet newPet;

	@BeforeEach
	void setup() {
		owner = new Owner();

		// Pet existente con ID
		pet1 = new Pet();
		pet1.setName("Lucky");
		pet1.setId(10);
		owner.addPet(pet1);

		// Duplicado mismo nombre
		pet2 = new Pet();
		pet2.setName("Lucky");
		pet2.setId(11);
		owner.addPet(pet2);

		// Pet nuevo (sin ID)
		newPet = new Pet();
		newPet.setName("Bobby");
		owner.addPet(newPet);
	}

	// Buscando por nombre registrado
	@Test
	void shouldReturnPetByName() {
		Pet result = owner.getPet("Lucky");
		assertThat(result).isNotNull();
		assertThat(result.getName()).isEqualTo("Lucky");
	}

	// Buscar por nombre no registrado
	@Test
	void shouldReturnNullWhenNameNotFound() {
		Pet result = owner.getPet("Rocky");
		assertThat(result).isNull();
	}

	// Probando case insensitive
	@Test
	void shouldIgnoreCaseWhenSearchingByName() {
		Pet result = owner.getPet("lUcKy");
		assertThat(result).isNotNull();
	}

	// defecto SUT: retorna el último en caso de duplicados
	@Test
	void shouldReturnLastPetWhenThereAreDuplicates() {
		Pet result = owner.getPet("Lucky");
		assertThat(result).isEqualTo(pet2); // comportamiento real detectado
	}

	// ignoreNew = true, debe ignorar mascotas nuevas
	@Test
	void shouldReturnNullForNewPetWhenIgnored() {
		Pet result = owner.getPet("Bobby", true);
		assertThat(result).isNull();
	}

	// ignoreNew = false, debe devolver mascotas nuevas
	@Test
	void shouldReturnNewPetWhenNotIgnored() {
		Pet result = owner.getPet("Bobby", false);
		assertThat(result).isEqualTo(newPet);
	}

	// Defecto SUT: getPet(ID) no encuentra mascota aunque coincida el ID
	@Test
	void shouldFailToFindPetByIdEvenIfExists() {
		Pet result = owner.getPet(10);
		assertThat(result).isNull(); // comportamiento defectuoso del SUT
	}

}
