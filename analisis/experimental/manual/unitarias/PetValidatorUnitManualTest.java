package org.springframework.samples.petclinic.experimental.manual.unitarias.model;

import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;

import org.junit.jupiter.api.Test;
import org.springframework.samples.petclinic.owner.Pet;
import org.springframework.samples.petclinic.owner.PetType;
import org.springframework.samples.petclinic.owner.PetValidator;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.validation.Errors;

class PetValidatorUnitManualTest {

	private final PetValidator validator = new PetValidator();

	private Errors validatePet(Pet pet) {
		Errors errors = new BeanPropertyBindingResult(pet, "pet");
		validator.validate(pet, errors);
		return errors;
	}

	@Test
	void shouldRejectEmptyName() {
		Pet pet = createPet("", new PetType(), LocalDate.now(), true);
		Errors errors = validatePet(pet);
		assertTrue(errors.hasFieldErrors("name"));
	}

	@Test
	void shouldRejectNameWithSpacesOnly() {
		Pet pet = createPet("   ", new PetType(), LocalDate.now(), true);
		Errors errors = validatePet(pet);
		assertTrue(errors.hasFieldErrors("name"));
	}

	@Test
	void shouldAcceptValidName() {
		Pet pet = createPet("Lucky", new PetType(), LocalDate.now(), true);
		Errors errors = validatePet(pet);
		assertFalse(errors.hasErrors());
	}

	@Test
	void shouldRejectNullTypeForNewPet() {
		Pet pet = createPet("Lucky", null, LocalDate.now(), true);
		Errors errors = validatePet(pet);
		assertTrue(errors.hasFieldErrors("type"));
	}

	@Test
	void shouldNotRejectTypeForExistingPet() {
		Pet pet = createPet("Lucky", null, LocalDate.now(), false);
		pet.setId(10);
		Errors errors = validatePet(pet);
		assertFalse(errors.hasFieldErrors("type"));
	}

	@Test
	void shouldRejectNullBirthDate() {
		Pet pet = createPet("Lucky", new PetType(), null, true);
		Errors errors = validatePet(pet);
		assertTrue(errors.hasFieldErrors("birthDate"));
	}

	@Test
	void shouldThrowExceptionWhenObjectIsNull() {
		assertThrows(NullPointerException.class, () -> validator.validate(null, null));
	}

	private Pet createPet(String name, PetType type, LocalDate birthDate, boolean isNew) {
		Pet pet = new Pet();
		pet.setName(name);
		pet.setType(type);
		pet.setBirthDate(birthDate);
		if (!isNew) {
			pet.setId(10);
		}
		return pet;
	}

}
